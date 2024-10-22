from django.contrib import admin
from .models import Client, Expenses, SplitDetail

# Register your models here.
@admin.register(Client,Expenses, SplitDetail )
class ClientAdmin(admin.ModelAdmin):
    class Meta:
        model = Client
        fields ='__all__'

class ExpensesAdmin(admin.ModelAdmin):
    class Meta:
        model =Expenses
        fields = '__all__'

class SplitDetailsAdmin(admin.ModelAdmin):
    class Meta:
        model = SplitDetail
        fields = '__all__'
