from rest_framework import generics, status
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from activity.models import Todo, Note, Journal
from api.activity.serializers import TodoSerializer, NoteSerializer, JournalSerializer
from api.activity.filters import TodoFilter, NoteFilter, JournalFilter

from core.utils import api_response


# --------------------------------------------------
# TODOO LIST & CREATE
# --------------------------------------------------
class TodoListView(generics.ListCreateAPIView):
    queryset = Todo.active_objects.all()
    serializer_class = TodoSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TodoFilter
    ordering_fields = ["title", "priority", "due_date", "date_added"]
    ordering = ["-auto_id"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": Todo.active_objects.count(),
            "completed": Todo.active_objects.filter(is_completed=True).count(),
            "pending": Todo.active_objects.filter(is_completed=False).count(),
            "high_priority": Todo.active_objects.filter(priority="high").count(),
        }

        return api_response(
            message="Todos retrieved successfully",
            data={"todos": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Todo created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create todo",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# TODOO RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class TodoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.active_objects.all()
    serializer_class = TodoSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Todo retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Todo updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update todo",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Todo deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )


# --------------------------------------------------
# NOTEE LIST & CREATE
# --------------------------------------------------
class NoteListView(generics.ListCreateAPIView):
    queryset = Note.active_objects.all()
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = NoteFilter
    ordering_fields = ["title", "is_pinned", "date_added"]
    ordering = ["-is_pinned", "-auto_id"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": Note.active_objects.count(),
            "pinned": Note.active_objects.filter(is_pinned=True).count(),
            "unpinned": Note.active_objects.filter(is_pinned=False).count(),
        }

        return api_response(
            message="Notes retrieved successfully",
            data={"notes": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Note created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create note",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# NOTEE RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.active_objects.all()
    serializer_class = NoteSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Note retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Note updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update note",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Note deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )


# --------------------------------------------------
# JOURNAL LIST & CREATE
# --------------------------------------------------
class JournalListView(generics.ListCreateAPIView):
    queryset = Journal.active_objects.all()
    serializer_class = JournalSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = JournalFilter
    ordering_fields = ["title", "date", "mood", "date_added"]
    ordering = ["-date"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = self.get_serializer(queryset, many=True).data

        stats = {
            "total": Journal.active_objects.count(),
            "great": Journal.active_objects.filter(mood="great").count(),
            "good": Journal.active_objects.filter(mood="good").count(),
            "neutral": Journal.active_objects.filter(mood="neutral").count(),
            "bad": Journal.active_objects.filter(mood="bad").count(),
            "terrible": Journal.active_objects.filter(mood="terrible").count(),
        }

        return api_response(
            message="Journals retrieved successfully",
            data={"journals": data, "stats": stats},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Journal created successfully",
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )
        else:
            return api_response(
                message="Failed to create journal",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )


# --------------------------------------------------
# JOURNAL RETRIEVE, UPDATE & DELETE
# --------------------------------------------------
class JournalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Journal.active_objects.all()
    serializer_class = JournalSerializer
    lookup_field = "slug"

    def retrieve(self, request, *args, **kwargs):
        return api_response(
            message="Journal retrieved successfully",
            data=self.get_serializer(self.get_object()).data,
            status=status.HTTP_200_OK
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=kwargs.get("partial", False)
        )
        if serializer.is_valid():
            serializer.save()
            return api_response(
                message="Journal updated successfully",
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        else:
            return api_response(
                message="Failed to update journal",
                status=status.HTTP_400_BAD_REQUEST,
                serializer=serializer
            )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            message="Journal deleted successfully",
            status=status.HTTP_204_NO_CONTENT
        )