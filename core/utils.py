from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from activity.models import Task, DailyTask
from django.db import transaction as db_transaction
from decimal import Decimal
from finance.models import BankAccount, Transaction, SelfTransfer
from django.db.models import Sum

def api_response(message="", status=status.HTTP_200_OK, data=None, serializer=None, general_errors=None):

    response = {
        "status": status,
        "message": {
            "title": "Success" if status < 400 else "Failed",
            "body": message if status < 400 else "An error occurred",
        }
    }

    errors = {"form_errors": {}, "general_errors": []}

    if serializer is not None:
        def flatten_errors(error_dict, prefix=""):
            for field, value in error_dict.items():
                key = f"{prefix}{field}"
                if isinstance(value, dict):
                    flatten_errors(value, f"{key}.")
                elif isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            flatten_errors(item, f"{key}.")
                        else:
                            errors["form_errors"].setdefault(key, []).append(str(item))

        flatten_errors(serializer.errors)

    if general_errors:
        if isinstance(general_errors, list):
            errors["general_errors"].extend(general_errors)
        else:
            errors["general_errors"].append(str(general_errors))

    if status >= 400:
        response["errors"] = errors

    if data is not None:
        response["data"] = data

    return Response(response, status=status)


def ensure_daily_tasks_created():
    today = datetime.today()

    # Check if already created today
    if DailyTask.objects.filter(date=today).exists():
        return

    tasks = Task.objects.filter(is_deleted=False)
    for task in tasks:
        DailyTask.objects.get_or_create(task=task, date=today)


def update_account_balance():
    accounts = BankAccount.active_objects.all()

    for account in accounts:
        income       = Transaction.active_objects.filter(account=account, type="income" ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        expense      = Transaction.active_objects.filter(account=account, type="expense").aggregate(total=Sum("amount"))["total"] or Decimal("0")
        transfers_in = SelfTransfer.active_objects.filter(to_account=account  ).aggregate(total=Sum("amount"))["total"] or Decimal("0")
        transfers_out= SelfTransfer.active_objects.filter(from_account=account).aggregate(total=Sum("amount"))["total"] or Decimal("0")

        account.balance = income - expense + transfers_in - transfers_out
        account.save()
