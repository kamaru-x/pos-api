from django.contrib import admin
from finance.models import BankAccount, TransactionCategory, Transaction, SelfTransfer


# --------------------------------------------------
# BANK ACCOUNT
# --------------------------------------------------
@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display  = ("name", "bank_name", "account_number", "balance", "is_deleted", "creator", "date_added")
    list_filter   = ("is_deleted",)
    search_fields = ("name", "bank_name", "account_number")
    ordering      = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Account Info", {
            "fields": ("name", "bank_name", "account_number", "balance", "note")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )


# --------------------------------------------------
# TRANSACTION CATEGORY
# --------------------------------------------------
@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display  = ("name", "is_deleted", "creator", "date_added")
    list_filter   = ("is_deleted",)
    search_fields = ("name",)
    ordering      = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Category Info", {
            "fields": ("name", "type")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )


# --------------------------------------------------
# TRANSACTION
# --------------------------------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display  = ("title", "account", "category", "type", "amount", "date", "is_deleted", "creator", "date_added")
    list_filter   = ("type", "is_deleted", "date", "category")
    search_fields = ("title", "note")
    list_editable = ("type",)
    date_hierarchy = "date"
    ordering      = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Transaction Info", {
            "fields": ("title", "account", "category", "type", "amount", "date", "note")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )


# --------------------------------------------------
# SELF TRANSFER
# --------------------------------------------------
@admin.register(SelfTransfer)
class SelfTransferAdmin(admin.ModelAdmin):
    list_display  = ("from_account", "to_account", "amount", "date", "is_deleted", "creator", "date_added")
    list_filter   = ("is_deleted", "date")
    search_fields = ("from_account__name", "to_account__name", "note")
    date_hierarchy = "date"
    ordering      = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Transfer Info", {
            "fields": ("from_account", "to_account", "amount", "date", "note")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )