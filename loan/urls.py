from django.urls import path
from .views import *

urlpatterns = [
    path('loan/', loan_dashboard, name='loan_dashboard'),
    path('add-borrower/', add_borrower, name='add_borrower'),
    path('add-loan/', add_loan, name='add_loan'),
    path('add-payment/', add_payment, name='add_payment'),
]