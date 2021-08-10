from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

from OnlineBedBookingSystem.custom import *
from userapp.models import Account


class Hospital(models.Model):

    name                    = models.CharField(max_length=255, unique=True, primary_key=True)
    slug                    = models.SlugField(blank=True, null=True) 
    hospital_id             = models.CharField(max_length=255, unique=True, primary_key=False)
    TYPE_CHOICE             =   (
                                    ('government', 'Government'),
                                    ('private', 'Private'),
                                )
    hospital_type           = models.CharField(max_length=12, choices=TYPE_CHOICE, default='government')
    email                   = models.EmailField()
    help_line               = models.CharField(max_length=17)
    state                   = models.CharField(max_length=50)
    city                    = models.CharField(max_length=50)
    address                 = models.TextField()
    user                    = models.OneToOneField(Account(), on_delete=models.CASCADE)
    word_bed                = models.IntegerField(default=0)
    icu_bed                 = models.IntegerField(default=0)
    created_at              = models.DateTimeField(default=timezone.now)
    updated_at              = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def get_type(self):
        return self.hospital_type

    class Meta:
        verbose_name = 'Hospital'
        verbose_name_plural = 'Hospitals'
        ordering = ['name',]

@receiver(pre_save, sender=Hospital)
def _pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_through_name(instance)

