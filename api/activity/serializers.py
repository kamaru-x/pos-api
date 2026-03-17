from rest_framework import serializers
from core.mixins import RepMixin
from activity.models import Todo, Note, Journal, Task, DailyTask


# --------------------------------------------------
# TODOO SERIALIZER
# --------------------------------------------------
class TodoSerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model = Todo
        fields = [
            'id', 'slug', 'title', 'description', 'priority',
            'is_completed', 'due_date', 'date_added', 'date_updated'
        ]


# --------------------------------------------------
# NOTEE SERIALIZER
# --------------------------------------------------
class NoteSerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = [
            'id', 'slug', 'title', 'content',
            'is_pinned', 'date_added', 'date_updated'
        ]


# --------------------------------------------------
# JOURNAL SERIALIZER
# --------------------------------------------------
class JournalSerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model = Journal
        fields = [
            'id', 'slug', 'title', 'content',
            'date', 'mood', 'date_added', 'date_updated'
        ]


# --------------------------------------------------
# TASK SERIALIZER
# --------------------------------------------------
class TaskSerializer(RepMixin, serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id', 'slug', 'title'
        ]


# --------------------------------------------------
# DAILY TASK SERIALIZER
# --------------------------------------------------
class DailyTaskSerializer(RepMixin, serializers.ModelSerializer):
    task    = TaskSerializer(read_only=True)
    task_id = serializers.PrimaryKeyRelatedField(queryset=Task.objects.filter(is_deleted=False), source="task", write_only=True)

    class Meta:
        model = DailyTask
        fields = [
            'id', 'slug', 'date', 'task', 'task_id', 'is_completed', 'date_added', 'date_updated'
        ]