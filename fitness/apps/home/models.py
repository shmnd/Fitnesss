from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.
class AbstractDateFieldMix(models.Model):
    created_date     = models.DateTimeField(_('created_date'), auto_now_add=True, editable=False, blank=True, null=True)
    modified_date    = models.DateTimeField(_('modified_date'), auto_now=True, editable=False, blank=True, null=True)

    class Meta:
        abstract = True


class FitnessClass(AbstractDateFieldMix):
    class FitnessType(models.TextChoices):
        yoga    = 'Yoga'
        zumba   = 'Zumba'
        hitt    = 'HIIT'
    
    fitness_name = models.CharField(_('Fitness category name'), choices=FitnessType.choices, null=True, blank=True)
    datetime = models.DateTimeField(_('Date and Time'),null=True, blank=True)
    instructor   = models.CharField(_('Fitness trainer name'),max_length=100, null=True, blank=True)
    total_slots  = models.PositiveIntegerField(_('Fitness total slots'), null=True, blank=True)
    available_slots = models.PositiveIntegerField(_('Fitness available slots'), null=True, blank=True)
    class Meta:
        verbose_name          = "Fitness"
        verbose_name_plural   = "Fitnesses"


class Booking(AbstractDateFieldMix):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, null= True, blank= True)
    client_name = models.CharField(_('Client name'),max_length=100,null= True, blank= True)
    client_email = models.EmailField(_('Client email'),null= True, blank= True)

    class Meta:
        verbose_name          = "Booking"
        verbose_name_plural   = "Bookings"


