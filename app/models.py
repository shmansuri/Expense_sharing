from django.db import models

# Create your models here.
class Client(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100, unique=True)
    mobile = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name
    

class Expenses(models.Model):
    expenses_choice=(
        ('equal','Equal split'),
        ('exact', 'Exact split'),
        ('percentage', 'Percentage split')
    )
    description=models.CharField(max_length=200)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2)
    creator = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='expenses')
    participants = models.ManyToManyField(Client, related_name='sharing_expenses')
    split_method = models.CharField(max_length=15, choices=expenses_choice)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description


class SplitDetail(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='split_details')
    expense = models.ForeignKey(Expenses, on_delete=models.CASCADE, related_name='split_details')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} owes {self.amount_owed} for {self.expense.description}"