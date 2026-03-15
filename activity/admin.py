from django.contrib import admin
from .models import Todo, Note, Journal


# --------------------------------------------------
# TODOO
# --------------------------------------------------
@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "priority", "is_completed", "due_date", "is_deleted", "creator", "date_added")
    list_filter = ("priority", "is_completed", "is_deleted", "due_date")
    search_fields = ("title", "description")
    list_editable = ("is_completed", "priority")
    date_hierarchy = "due_date"
    ordering = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Task Info", {
            "fields": ("title", "description", "priority")
        }),
        ("Status", {
            "fields": ("is_completed", "due_date")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )


# --------------------------------------------------
# NOTEE
# --------------------------------------------------
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "is_pinned", "is_deleted", "creator", "date_added", "date_updated")
    list_filter = ("is_pinned", "is_deleted")
    search_fields = ("title", "content")
    list_editable = ("is_pinned",)
    ordering = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Note Info", {
            "fields": ("title", "content", "is_pinned")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )


# --------------------------------------------------
# JOURNAL
# --------------------------------------------------
@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "mood", "is_deleted", "creator", "date_added")
    list_filter = ("mood", "is_deleted", "date")
    search_fields = ("title", "content")
    date_hierarchy = "date"
    ordering = ("-auto_id",)
    readonly_fields = ("id", "auto_id", "slug", "creator", "updater", "date_added", "date_updated", "is_deleted")
    fieldsets = (
        ("Journal Info", {
            "fields": ("title", "content", "date", "mood")
        }),
        ("Metadata", {
            "fields": ("id", "auto_id", "slug", "is_deleted"),
            "classes": ("collapse",)
        }),
        ("Timestamps & Users", {
            "fields": ("creator", "updater", "date_added", "date_updated"),
            "classes": ("collapse",)
        }),
    )