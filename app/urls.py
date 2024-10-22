from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientViewSet, ExpensesViewSet,SplitDetailViewSet

router = DefaultRouter()
router.register(r'Clients', ClientViewSet)
router.register(r'Expenses', ExpensesViewSet)
router.register(r'split_details', SplitDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]