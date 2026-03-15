from django.db import models
from django.utils.translation import gettext_lazy as _

class TodoPriorityChoices(models.TextChoices):
    LOW = 'low', _('Low')
    NORMAL = 'normal', _('Normal')
    HIGH = 'high', _('High')

class JournalMoodChoices(models.TextChoices):
    GREAT = 'great', _('Great')
    GOOD = 'good', _('Good')
    NEUTRAL = 'neutral', _('Neutral')
    BAD = 'bad', _('Bad')
    TERRIBLE = 'terrible', _('Terribble')