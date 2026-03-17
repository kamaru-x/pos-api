from django.db.models import Q
from django_filters import rest_framework as filters

from activity.models import Todo, Note, Journal, Task, DailyTask

from core.choices import TodoPriorityChoices, JournalMoodChoices

# --------------------------------------------------
# TODOO FILTER
# --------------------------------------------------
class TodoFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    priority = filters.ChoiceFilter(choices=TodoPriorityChoices.choices)
    is_completed = filters.BooleanFilter()
    due_date = filters.DateFilter()
    due_date_from = filters.DateFilter(field_name='due_date', lookup_expr='gte')
    due_date_to = filters.DateFilter(field_name='due_date', lookup_expr='lte')

    class Meta:
        model = Todo
        fields = ['priority', 'is_completed', 'due_date']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(description__icontains=value)
        )


# --------------------------------------------------
# NOTEE FILTER
# --------------------------------------------------
class NoteFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    is_pinned = filters.BooleanFilter()

    class Meta:
        model = Note
        fields = ['is_pinned']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(content__icontains=value)
        )


# --------------------------------------------------
# JOURNAL FILTER
# --------------------------------------------------
class JournalFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    mood = filters.ChoiceFilter(choices=JournalMoodChoices.choices)
    date = filters.DateFilter()
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Journal
        fields = ['mood', 'date']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) |
            Q(content__icontains=value)
        )
    

# --------------------------------------------------
# TASK FILTER
# --------------------------------------------------
class TaskFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')

    class Meta:
        model = Task
        fields = ['title']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
        )


# --------------------------------------------------
# DAILY TASK FILTER
# --------------------------------------------------
class DailyTaskFilter(filters.FilterSet):
    search       = filters.CharFilter(method='search_filter')
    is_completed = filters.BooleanFilter()
    date         = filters.DateFilter()
    date_from    = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to      = filters.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = DailyTask
        fields = ['is_completed', 'date']

    def search_filter(self, queryset, name, value):
        return queryset.filter(
            Q(task__title__icontains=value)
        )