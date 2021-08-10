from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from userapp.models import Account
from hospital.models import Hospital
from OnlineBedBookingSystem.custom import *


class BookingRequest(models.Model):

    from_user                       = models.ForeignKey(Account, on_delete=models.CASCADE)
    to_hospital                     = models.ManyToManyField(Hospital)
    bed_type                        = models.CharField(max_length=10)
    adhar                           = models.CharField(max_length=50, unique=True)
    created_at                      = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'BookingRequest'
        verbose_name_plural = 'BookingRequests'
        ordering = ['created_at',]


class TempPatientDetails(models.Model):

    reference_user                  = models.ForeignKey(Account, verbose_name=("reference user"), on_delete=models.SET_NULL, null=True)
    hospital                        = models.ManyToManyField(Hospital)
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

@receiver(pre_save, sender=TempPatientDetails)
def _pre_save_receiver(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator_through_name(instance)

@receiver(post_save, sender=TempPatientDetails)
def _post_save_receiver(sender, instance, **kwargs):
    # create new booking_request obj
    booking_request_obj = BookingRequest.objects.create(
        from_user = instance.reference_user,
        bed_type = instance.bed,
        adhar = instance.adhar
    )


class ConformRequest(models.Model):

    request                         = models.ForeignKey(BookingRequest, on_delete=models.CASCADE)
    user                            = models.ForeignKey(Account, verbose_name='Who confirm the request?', on_delete=models.CASCADE)
    created_at                      = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'ConfirmRequest'
        verbose_name_plural = 'ConfirmRequests'
        ordering = ['-created_at',]


class CancelRequest(models.Model):

    request                         = models.ForeignKey(BookingRequest, on_delete=models.CASCADE)
    user                            = models.ForeignKey(Account, verbose_name='Who cancel the request?', on_delete=models.CASCADE)
    created_at                      = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.request)

    class Meta:
        verbose_name = 'CancelRequest'
        verbose_name_plural = 'CancelRequests'
        ordering = ['-created_at',]


class Thread(models.Model):
    user                            = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)
    unique_room_id                  = models.CharField(max_length=10, null=True, blank=True)
    timestamp                       = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.unique_room_id

    class Meta:
        verbose_name = 'Thread'
        verbose_name_plural = 'Threads'
        ordering = ['-timestamp']    

@receiver(pre_save, sender=Thread)
def _pre_save_receiver(sender, instance, **kwargs):
    if not instance.unique_room_id:
        instance.unique_room_id = unique_room_genarator(instance)


class Notification(models.Model):
    notification_body               = models.TextField(blank=True, null=True)
    hospital_id                     = models.CharField(max_length=255, blank=True, null=True)
    booking_request                 = models.ForeignKey(BookingRequest, on_delete=models.CASCADE, blank=True, null=True)
    show                            = models.BooleanField(default=True)
    timestamp                       = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
@receiver(post_save, sender=Notification)
def _post_save_receiver(sender, created, instance, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        
        hospital = Hospital.objects.get(hospital_id=instance.hospital_id)
        thread = Thread.objects.get(user=hospital.user.pk)
        room_name = thread.unique_room_id

        async_to_sync(channel_layer.group_send)(
            room_name, {
                'type': 'send_notification',
                'notification': instance.notification_body,
                'id': str(instance.pk)
            }
        )
        

class Activity(models.Model):
    user                             = models.ForeignKey(Account, on_delete=models.CASCADE)
    text                             = models.CharField(max_length=300)
    timestamp                        = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'User Activity'
        verbose_name_plural = 'User Activities'    
        ordering = ['-timestamp',]



