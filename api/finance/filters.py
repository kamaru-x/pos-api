import django_filters as filters
from django.db.models import Q
from finance.models import BankAccount, TransactionCategory, Transaction, TransactionTypeChoices, SelfTransfer


# --------------------------------------------------
# BANK ACCOUNT FILTER
# --------------------------------------------------
class BankAccountFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')

    class Meta:
        model  = BankAccount
        fields = ['name']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)       |
            Q(bank_name__icontains=value)  |
            Q(account_number__icontains=value)
        )


# --------------------------------------------------
# TRANSACTION CATEGORY FILTER
# --------------------------------------------------
class TransactionCategoryFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    type = filters.ChoiceFilter(choices=TransactionTypeChoices.choices)

    class Meta:
        model  = TransactionCategory
        fields = ['name', 'type']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )


# --------------------------------------------------
# TRANSACTION FILTER
# --------------------------------------------------
class TransactionFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    type = filters.ChoiceFilter(choices=TransactionTypeChoices.choices)
    account = filters.UUIDFilter(field_name='account__id')
    category  = filters.UUIDFilter(field_name='category__id')
    date = filters.DateFilter()
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model  = Transaction
        fields = ['type', 'account', 'category', 'date']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(note__icontains=value)
        )
    

# --------------------------------------------------
# SELF TRANSFER FILTER
# --------------------------------------------------
class SelfTransferFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    from_account = filters.UUIDFilter(field_name='from_account__id')
    to_account = filters.UUIDFilter(field_name='to_account__id')
    date = filters.DateFilter()
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model  = SelfTransfer
        fields = ['from_account', 'to_account', 'date']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(from_account__name__icontains=value) |
            Q(to_account__name__icontains=value)   |
            Q(note__icontains=value)
        )