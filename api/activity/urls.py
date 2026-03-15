from django.urls import path
from . import views

app_name = 'api_activity'

urlpatterns = [
    # --------------------------------------------------
    # TODOO
    # --------------------------------------------------
    path('todos/', views.TodoListView.as_view(), name='todo-list'),
    path('todos/<slug:slug>/', views.TodoDetailView.as_view(), name='todo-detail'),

    # --------------------------------------------------
    # NOTEE
    # --------------------------------------------------
    path('notes/', views.NoteListView.as_view(), name='note-list'),
    path('notes/<slug:slug>/', views.NoteDetailView.as_view(), name='note-detail'),

    # --------------------------------------------------
    # JOURNAL
    # --------------------------------------------------
    path('journals/', views.JournalListView.as_view(), name='journal-list'),
    path('journals/<slug:slug>/', views.JournalDetailView.as_view(), name='journal-detail'),
]