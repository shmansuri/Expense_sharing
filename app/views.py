import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Client, Expenses, SplitDetail
from .serializers import ClientSerializer, ExpensesSerializer, SplitDetailSerializer


# ViewSet for Client model
class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


# ViewSet for Expenses model
class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer

 


    @action(detail=False, methods=['get'])
    def user_expenses(self, request):
        """
        Show individual expenses for a specific user.
        URL: /api/expenses/user_expenses/?user_id=<id>
        """

        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(Client, pk=user_id)
            expenses_as_creator = Expenses.objects.filter(creator=user)
            expenses_as_participant = Expenses.objects.filter(participants=user)
            all_expenses= expenses_as_creator| expenses_as_participant
            serializer = self.get_serializer(all_expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        expenses = Expenses.objects.all()
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(detail=False, methods=['get'])
    def download_balance_sheet(self, request):
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(Client, pk=user_id)
            split_detail = SplitDetail.objects.filter(user=user)
            filename = f"{user.name}_balance_sheet.csv"
            clientname= f"{user.name}'s share"
        else:
            split_detail = SplitDetail.objects.all()
            filename = "overall_balance_sheet.csv"
            clientname = "participant's share"

        # Create the HTTP response with CSV content
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        # user_column = f"{user.name}'s Share" if user else "Share"
        writer = csv.writer(response)
        writer.writerow(['Expense Description', 'Total Amount', 'Creator', clientname, 'Percentage','date'])

        # Write each expense with details to the CSV
        for sd in split_detail:
            
            writer.writerow([
                sd.expense.description,
                sd.expense.total_amount,
                sd.expense.creator.name,
                sd.amount_owed,
                f"{sd.percentage}%" if sd.percentage else 'N/A',
                sd.expense.date.strftime('%y-%m-%d %H:%M')
                ])

        return response


# ViewSet for SplitDetail model
class SplitDetailViewSet(viewsets.ModelViewSet):
    queryset = SplitDetail.objects.all()
    serializer_class = SplitDetailSerializer

    @action(detail=False, methods=['get'])
    def list_user_split_details(self, request):
        """
        List all split details for a particular user.
        URL: /api/splitdetails/list_user_split_details/?user_id=<id>
        """
        user_id = request.query_params.get('user_id')
        if user_id:
            user = get_object_or_404(Client, pk=user_id)
            split_details = SplitDetail.objects.filter(user=user)
            serializer = self.get_serializer(split_details, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'user_id query parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)

