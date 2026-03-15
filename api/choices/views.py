from core.choices import TodoPriorityChoices, JournalMoodChoices

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

def serialize_choices(choices_cls):
    return [
        {"id": choice.value, "label": choice.label}
        for choice in choices_cls
    ]

CHOICES_MAP = {
    "todo-priorities": TodoPriorityChoices,
    "journal-moods": JournalMoodChoices
}

# --------------------------------------------------
# CHOICES API
# --------------------------------------------------
class ChoicesAPIView(APIView):

    def get(self, request):
        keys = request.query_params.get("keys")

        if not keys:
            return Response({
                key: serialize_choices(choice_cls)
                for key, choice_cls in CHOICES_MAP.items()
            })

        response = {}
        for key in keys.split(","):
            key = key.strip()
            if key in CHOICES_MAP:
                response[key] = serialize_choices(CHOICES_MAP[key])

        return Response(response)

# --------------------------------------------------
# CLIENT CHOICES
# --------------------------------------------------
# class ClientChoices(generics.ListAPIView):
#     queryset = Client.active_objects.all()
#     serializer_class = ClientMinimalSerializer