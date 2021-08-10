from django.contrib import admin

from bookpatient.models import BookingRequest, CancelRequest, ConformRequest, Notification, TempPatientDetails, Thread, Notification, Activity

admin.site.register(BookingRequest)
admin.site.register(CancelRequest)
admin.site.register(ConformRequest)
admin.site.register(TempPatientDetails)
admin.site.register(Thread)
admin.site.register(Notification)
admin.site.register(Activity)


