from django.urls import path
from .views import *

urlpatterns = [
    path('categories/', category_list, name='category_list'),
    path('categories/delete/<int:pk>/', delete_category, name='delete_category'),
    path('transactions/', transaction_list, name='transaction_list'),
    path('invoices/', invoice_list, name='invoice_list'),
    path('balance-sheet/', balance_sheet_view, name='balance_sheet'),
    path('balance-sheet/pdf/', balance_sheet_pdf, name='balance_sheet_pdf'),
    path('balance-sheet/excel/', export_balance_sheet_excel, name='balance_sheet_excel'),

    path('income-statement/', income_statement_view, name='income_statement'),
    path('income-statement/pdf/', income_statement_pdf, name='income_statement_pdf'),
    path('income-statement/excel/', export_income_statement_excel, name='income_statement_excel'),

    path('ledger/<int:account_id>/', ledger_view, name='ledger_view'),
    path('ledger/<int:account_id>/pdf/', ledger_pdf, name='ledger_pdf'),
    path('ledger/<int:account_id>/excel/', ledger_excel, name='ledger_excel'),
    path('ledger/', ledger_list, name='ledger_list')

]
