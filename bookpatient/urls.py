from django.urls import path

from .api import BookBedAPI

app_name = 'bookpatient'

urlpatterns = [
    path('add-new-bed/', BookBedAPI.as_view(), name='book_new_bed'),
]

