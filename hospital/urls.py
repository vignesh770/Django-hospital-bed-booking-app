from django.urls import path

from .views import *
from .api import *


app_name = 'hospital'


urlpatterns = [
    # path for view
    path('registration', HospitalRegistrationView.as_view(), name='registration'),
    path('authority-login', HospitalLoginView.as_view(), name='login'),
    path('authority-dashboard', HospitalDashboardView.as_view(), name='dashboard'),
    path('<slug:slug>', HospitalDetailView.as_view(), name='hospital_detail'),

    # path for api
    path('register-new-hospital/', CreateHospital.as_view(), name='register_new_hospital'),
    path('login-hospital-authority/', HospitalAuthorityLoginAPI.as_view(), name='authority_login'),
    path('logout/logout-hospital-authority', HospitalAuthorityLogoutAPI.as_view(), name='authority_logout'),
    path('get-patients/<slug:status>', PatientListView.as_view(), name='get_patients'),
    path('update-bed/', UpdateBedAPI.as_view(), name='update_bed'),
    path('get-patient-info/<slug:slug>', PatientDetailView.as_view(), name='patient_details'),
    path('bed-details/<slug:slug>', HospitalBedDetalAPI.as_view(), name='bed_details'),
    path('add-patient/', AddPatientAPI.as_view(), name='add_patient'),
]

