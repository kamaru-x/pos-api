from django.db import models
from django.utils.translation import gettext as _

from core.models import BaseModel, save_data
from core.middlewares import RequestMiddleware
from core.choices import TodoPriorityChoices, JournalMoodChoices


# --------------------------------------------------
# TODOO
# --------------------------------------------------
class Todo(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(max_length=20, choices=TodoPriorityChoices.choices, default=TodoPriorityChoices.NORMAL)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Todo")
        verbose_name_plural = _("Todos")
        ordering = ("-auto_id",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)
        super(Todo, self).save(*args, **kwargs)


# --------------------------------------------------
# NOTEE
# --------------------------------------------------
class Note(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_pinned = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        ordering = ("-auto_id",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)
        super(Note, self).save(*args, **kwargs)


# --------------------------------------------------
# JOURNAL
# --------------------------------------------------
class Journal(BaseModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateField()
    mood = models.CharField(max_length=20, choices=JournalMoodChoices.choices, default=JournalMoodChoices.NEUTRAL)

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        verbose_name = _("Journal")
        verbose_name_plural = _("Journals")
        ordering = ("-date",)

    def save(self, request=None, *args, **kwargs):
        request = RequestMiddleware(get_response=None)
        request = request.thread_local.current_request
        save_data(self, request, self.title)
        super(Journal, self).save(*args, **kwargs)