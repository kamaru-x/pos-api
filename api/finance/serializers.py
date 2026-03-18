from rest_framework import serializers
from core.mixins import RepMixin
from finance.models import BankAccount, TransactionCategory, Transaction, SelfTransfer


# --------------------------------------------------
# BANK ACCOUNT SERIALIZER
# --------------------------------------------------
class BankAccountSerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model  = BankAccount
        fields = [
            'id', 'slug', 'name', 'bank_name', 'account_number', 'balance', 'note', 'date_added', 'date_updated'
        ]


# --------------------------------------------------
# TRANSACTION CATEGORY SERIALIZER
# --------------------------------------------------
class TransactionCategorySerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model  = TransactionCategory
        fields = [
            'id', 'slug', 'name', 'type', 'date_added', 'date_updated'
        ]


# --------------------------------------------------
# TRANSACTION SERIALIZER
# --------------------------------------------------
class TransactionSerializer(RepMixin, serializers.ModelSerializer):
    account = BankAccountSerializer(read_only=True)
    account_id = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.filter(is_deleted=False), source="account", write_only=True)
    category = TransactionCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=TransactionCategory.objects.filter(is_deleted=False), source="category", write_only=True)

    class Meta:
        model  = Transaction
        fields = [
            'id', 'slug', 'title', 'account', 'account_id', 'category', 'category_id',
            'type', 'amount', 'note', 'date', 'date_added', 'date_updated'
        ]


# --------------------------------------------------
# SELF TRANSFER SERIALIZER
# --------------------------------------------------
class SelfTransferSerializer(RepMixin, serializers.ModelSerializer):
    from_account = BankAccountSerializer(read_only=True)
    from_account_id = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.filter(is_deleted=False), source="from_account", write_only=True)
    to_account = BankAccountSerializer(read_only=True)
    to_account_id = serializers.PrimaryKeyRelatedField(queryset=BankAccount.objects.filter(is_deleted=False), source="to_account", write_only=True)

    class Meta:
        model  = SelfTransfer
        fields = [
            'id', 'slug', 'from_account', 'from_account_id',
            'to_account', 'to_account_id', 'amount', 'note',
            'date', 'date_added', 'date_updated'
        ]