import uuid
from django.db import models
from django.db.models import Max
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.conf import settings

# Create your models here.

def save_data(self, request, slug_string=None):
    if self._state.adding:
        self.auto_id = (self.__class__.objects.aggregate(max_auto_id=Max('auto_id')).get('max_auto_id') or 0) + 1
        if request.user.is_authenticated:
            self.creator = request.user
    else:
        if request.user.is_authenticated:
            self.updater = request.user
        self.date_updated = timezone.now()

    if slug_string and not self.slug:
        slug = slugify(slug_string)
        counter = 1
        temp_slug = slug
        while self.__class__.objects.filter(slug=temp_slug).exclude(pk=self.pk).exists():
            temp_slug = f'{slug}-{counter}'
            counter += 1
        self.slug = temp_slug

class ActiveManager(models.Manager):
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().exclude(is_deleted=True)

class DeletedManager(models.Manager):
    def get_queryset(self):
        return super(DeletedManager, self).get_queryset().filter(is_deleted=True)

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    auto_id = models.PositiveIntegerField(db_index=True, unique=True, editable=False, null=True, blank=True)

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,editable=False,related_name="creator_%(app_label)s_%(class)s_objects", limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    updater = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,editable=False, related_name="updater_%(app_label)s_%(class)s_objects", limit_choices_to={'is_active': True}, on_delete=models.CASCADE)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    date_updated = models.DateTimeField(null=True, blank=True,editable=False)
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveManager()
    deleted_objects = DeletedManager()

    class Meta:
        abstract = True
        default_permissions = ()