from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel, save_data
from core.middlewares import RequestMiddleware
from core.choices import TransactionTypeChoices


# --------------------------------------------------
# BANK ACCOUNT
# --------------------------------------------------
class BankAccount(BaseModel):
    name = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    bank_name = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("BankAccount")
        verbose_name_plural = _("BankAccount")
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)
        super(BankAccount, self).save(*args, **kwargs)


# --------------------------------------------------
# TRANSACTION CATEGORY
# --------------------------------------------------
class TransactionCategory(BaseModel):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=TransactionTypeChoices.choices)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = _("TransactionCategory")
        verbose_name_plural = _("TransactionCategory")
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.name)
        super(TransactionCategory, self).save(*args, **kwargs)


# --------------------------------------------------
# TRANSACTION
# --------------------------------------------------
class Transaction(BaseModel):
    account  = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transactions")
    category = models.ForeignKey(TransactionCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="transactions")
    title = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    type = models.CharField(max_length=10, choices=TransactionTypeChoices.choices)
    note = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.type} - {self.amount}"

    class Meta:
        verbose_name = _("Transaction")
        verbose_name_plural = _("Transaction")
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)
        super(Transaction, self).save(*args, **kwargs)


# --------------------------------------------------
# SELF TRANSFER
# --------------------------------------------------
class SelfTransfer(BaseModel):
    from_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transfers_out")
    to_account = models.ForeignKey(BankAccount, on_delete=models.CASCADE, related_name="transfers_in")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.from_account} → {self.to_account} ({self.amount})"

    class Meta:
        verbose_name = _("SelfTransfer")
        verbose_name_plural = _("SelfTransfer")
        ordering = ("-date_added",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, f"{self.from_account} to {self.to_account}")
        super(SelfTransfer, self).save(*args, **kwargs)