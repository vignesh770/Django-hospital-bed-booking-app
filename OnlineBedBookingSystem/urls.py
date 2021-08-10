from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from home.views import IndexView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('hospital/', include('hospital.urls', namespace='hospital')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('userapp/', include('userapp.urls', namespace='userapp')),
    path('bookpatient/', include('bookpatient.urls', namespace='bookpatient')),
    path('accounts/', include('allauth.urls')),
    path('', IndexView.as_view(), name='index'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

