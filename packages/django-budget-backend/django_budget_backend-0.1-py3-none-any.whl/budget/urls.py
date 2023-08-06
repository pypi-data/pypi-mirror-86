from django.urls import path

from api import views

urlpatterns = [
    path('budget', views.BudgetListCreateView.as_view(), name='budget-lc'),
    path('budget/<uuid:id>', views.BudgetRetrieveUpdateDestroyView.as_view(), name='budget-rud'),
    path('lineitem', views.LineItemListCreateView.as_view(), name='line-item-lc'),
    path('lineitem/<uuid:id>', views.LineItemRetrieveUpdateDestroyView.as_view(), name='line-item-rud'),
    path('transaction', views.TransactionListCreateView.as_view(), name='transaction-lc'),
    path('transaction/<uuid:id>', views.TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-rud')
]
