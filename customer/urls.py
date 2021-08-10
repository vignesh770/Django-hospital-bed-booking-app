from django.urls import path

from .views import *
from .api import *


app_name = 'customer'


urlpatterns = [
    # path for view
    path('login', CustomerLoginView.as_view(), name='customer_login'),
    path('registration', CustomerRegistrationView.as_view(), name='customer_registration'),
    path('dashboard', CustomerDashboardView.as_view(), name='customer_dashboard'),

    # path for api
    path('create-new-customer/', CustomerRegisterAPI.as_view(), name='create_new_customer'),
    path('customer-login/', CustomerLoginAPI.as_view(), name='customer_login_api'),
    path('customer-logout', CustomerLogoutAPIView.as_view(), name='customer_logout'),
    path('update-patient-info/', UpdatePatientDetailAPI.as_view(), name='update_patient_info'),
    path('add-temp-patient/', TempAddPatientAPI.as_view(), name='add_patient_temp'),
    path('search-hospitals', HospitalSearchAPI.as_view(), name='search_hospitals'),
]

