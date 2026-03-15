from django.db.models import Q
from django_filters import rest_framework as filters
from activity.models import Todo, Note, Journal


# --------------------------------------------------
# TODOO FILTER
# --------------------------------------------------
class TodoFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter')
    priority = filters.ChoiceFilter(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")])
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
    mood = filters.ChoiceFilter(choices=[
        ("great", "Great"), ("good", "Good"), ("neutral", "Neutral"),
        ("bad", "Bad"), ("terrible", "Terrible"),
    ])
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