from django.urls import path
from userapp.api import *

app_name = 'userapp'

urlpatterns = [
    path('get-user-details', UserDetailsAPIView.as_view(), name='user_details'),
]


