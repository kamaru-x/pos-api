from django.urls import path
from api.finance import views

app_name = 'api_finance'

urlpatterns = [
    # --------------------------------------------------
    # BANK ACCOUNT
    # --------------------------------------------------
    path('accounts/', views.BankAccountListView.as_view(), name='account-list'),
    path('accounts/<slug:slug>/', views.BankAccountDetailView.as_view(), name='account-detail'),

    # --------------------------------------------------
    # TRANSACTION CATEGORY
    # --------------------------------------------------
    path('categories/', views.TransactionCategoryListView.as_view(), name='category-list'),
    path('categories/overview/', views.TransactionCategoryOverviewView.as_view(), name='category-overview'),
    path('categories/<slug:slug>/', views.TransactionCategoryDetailView.as_view(), name='category-detail'),

    # --------------------------------------------------
    # TRANSACTION
    # --------------------------------------------------
    path('transactions/', views.TransactionListView.as_view(), name='transaction-list'),
    path('transactions/<slug:slug>/', views.TransactionDetailView.as_view(), name='transaction-detail'),

    # --------------------------------------------------
    # SELF TRANSFER
    # --------------------------------------------------
    path('transfers/', views.SelfTransferListView.as_view(), name='transfer-list'),
    path('transfers/<slug:slug>/', views.SelfTransferDetailView.as_view(), name='transfer-detail'),
]