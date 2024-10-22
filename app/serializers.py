from rest_framework import serializers
from .models import Client, Expenses, SplitDetail
from decimal import Decimal

# Client Serializer
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'mobile']

# SplitDetail Serializer (for output)
class SplitDetailSerializer(serializers.ModelSerializer):
    user = ClientSerializer(read_only=True)  # Display user details in nested representation

    class Meta:
        model = SplitDetail
        fields = ['id', 'user', 'amount_owed', 'percentage']

# Expense Serializer
class ExpensesSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=Client.objects.all())
    split_method = serializers.ChoiceField(choices=[('equal', 'Equal split'), ('exact', 'Exact split'), ('percentage', 'Percentage split')])

    # Flattened fields for input, allowing user_id and amount/percentage to be provided separately
    user_id_1 = serializers.IntegerField(write_only=True, required=False)
    user_id_2 = serializers.IntegerField(write_only=True, required=False)
    user_id_3 = serializers.IntegerField(write_only=True, required=False)
    percentage_1 = serializers.FloatField(write_only=True, required=False)
    percentage_2 = serializers.FloatField(write_only=True, required=False)
    percentage_3 = serializers.FloatField(write_only=True, required=False)
    amount_1 = serializers.FloatField(write_only=True, required=False)
    amount_2 = serializers.FloatField(write_only=True, required=False)
    amount_3 = serializers.FloatField(write_only=True, required=False)
    split_details_readonly = SplitDetailSerializer(source='split_details', many=True, read_only=True)

    class Meta:
        model = Expenses
        fields = [
            'id', 'description', 'total_amount', 'creator', 'participants', 
            'split_method', 'date', 'user_id_1', 'user_id_2', 'user_id_3',
            'percentage_1', 'percentage_2', 'percentage_3',
            'amount_1', 'amount_2', 'amount_3', 'split_details_readonly'
        ]
        read_only_fields = ['date', 'split_details_readonly']

    def validate(self, data):
        """
        Custom validation to ensure that the split details are valid based on the split method.
        """
        split_method = data.get('split_method')
        total_amount = data.get('total_amount')
        user_ids = [data.get('user_id_1'), data.get('user_id_2'), data.get('user_id_3')]
        user_ids = [uid for uid in user_ids if uid is not None]  # Filter out any None values

        if split_method == 'percentage':
            percentages = [
                data.get('percentage_1', 0),
                data.get('percentage_2', 0),
                data.get('percentage_3', 0)
            ]
            total_percentage = sum(percentages)
            if total_percentage != 100:
                raise serializers.ValidationError("Percentages must sum up to 100%.")
            if len(user_ids) != len([p for p in percentages if p > 0]):
                raise serializers.ValidationError("Each user must have a percentage if the split method is 'percentage'.")

        elif split_method == 'exact':
            amounts = [
                data.get('amount_1', 0),
                data.get('amount_2', 0),
                data.get('amount_3', 0)
            ]
            total_split = sum(amounts)
            if total_split != total_amount:
                raise serializers.ValidationError("Exact amounts do not sum up to the total amount.")
            if len(user_ids) != len([a for a in amounts if a > 0]):
                raise serializers.ValidationError("Each user must have a specified amount if the split method is 'exact'.")

        return data


    def create(self, validated_data):
        """
        Custom create method to handle the creation of an expense and its related SplitDetail entries.
        """
        # Extract fields used for split details
        user_ids = [validated_data.pop(f'user_id_{i}', None) for i in range(1, 4)]
        user_ids = [uid for uid in user_ids if uid is not None]

        amounts = [validated_data.pop(f'amount_{i}', None) for i in range(1, 4)]
        percentages = [validated_data.pop(f'percentage_{i}', None) for i in range(1, 4)]

        participants = validated_data.pop('participants', [])
        split_method = validated_data.get('split_method')
        total_amount = validated_data.get('total_amount')

        # Create the Expense object with the remaining validated data
        expense = Expenses.objects.create(**validated_data)
        expense.participants.set(participants)

        # Handle SplitDetail creation based on the split method
        if split_method == 'equal':
            amount_per_person = total_amount / len(user_ids)
            for user_id in user_ids:
                participant = Client.objects.get(id=user_id)
                SplitDetail.objects.create(
                    user=participant,
                    expense=expense,
                    amount_owed=amount_per_person
                )

        elif split_method == 'exact':
            for user_id, amount in zip(user_ids, amounts):
                if user_id and amount is not None:
                    participant = Client.objects.get(id=user_id)
                    SplitDetail.objects.create(
                        user=participant,
                        expense=expense,
                        amount_owed=Decimal(amount)
                    )

        elif split_method == 'percentage':
            for user_id, percentage in zip(user_ids, percentages):
                if user_id and percentage is not None:
                    participant = Client.objects.get(id=user_id)
                    amount_owed = (Decimal(percentage) / Decimal(100)) * total_amount
                    SplitDetail.objects.create(
                        user=participant,
                        expense=expense,
                        amount_owed=amount_owed,
                        percentage=Decimal(percentage)
                    )

        return expense
