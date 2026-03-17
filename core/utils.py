from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from activity.models import Task, DailyTask

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