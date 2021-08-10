from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

from OnlineBedBookingSystem.custom import *
from userapp.models import Account
from hospital.models import Hospital


class Patient(models.Model):

    reference_user                  = models.ForeignKey(Account, verbose_name=("reference user"), on_delete=models.SET_NULL, null=True)
    hospital                        = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    name                            = models.CharField(max_length=255, verbose_name='patient name')
    slug                            = models.SlugField(blank=True, null=True)
    GENDER_CHOICE                   = (
                                            ('male', 'Male'),
                                            ('female', 'Female')
                                        )
    gender                          = models.CharField(max_length=7, choices=GENDER_CHOICE, default='male')
    p_mobile                        = models.CharField(max_length=12, verbose_name='Primary mobile')
    s_mobile                        = models.CharField(max_length=12, verbose_name='Secondary mobile', blank=True, null=True)
    STATUS_CHOICE                   = (
                                            ('Alive', 'Alive'),
                                            ('Success', 'Success'),
                                            ('Dead', 'Dead')
                                        )
    status                          = models.CharField(max_length=20, choices=STATUS_CHOICE, default='Alive')
    adhar                           = models.CharField(max_length=50, unique=True)
    dob                             = models.DateField()
    BED_CHOICE                      = (
                                            ('word', 'Word'),
                                            ('icu', 'ICU')
                                        )
    bed                             = models.CharField(max_length=20, choices=BED_CHOICE, default='Word')
    created_at                      = models.DateTimeField(default=timezone.now)
    update_at                       = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def patient_status(self):
        return self.status

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        ordering = ['-created_at',]

@receiver(pre_save, sender=Patient)
def _pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_through_name(instance)

