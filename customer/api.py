from customer.models import Patient
from hospital.models import Hospital
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import serializers, status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q

from userapp.serializers import AccountRegisterSerializer
from .serializers import PatientSerializer
from bookpatient.models import BookingRequest, TempPatientDetails, Notification, Activity
from hospital.serializers import HospitalSerializer


class CustomerRegisterAPI(GenericAPIView):
    serializer_class = AccountRegisterSerializer

    def post(self, request):
        data = request.data
        data._mutable = True
        data['is_customer'] = True

        user_serializer = self.serializer_class(data=data)
        if user_serializer.is_valid():
            user_serializer.save()
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return Response({'user_deatils': user_serializer.data, 'login': True})
        else:
            return Response(user_serializer.errors)


class CustomerLoginAPI(GenericAPIView):
    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return Response({'login': True})
        return Response({'error': 'Incorrect login credentials.', 'login': False})


class CustomerLogoutAPIView(GenericAPIView):

    def get(self, request):
        user = request.user
        if user:
            logout(request)
        return redirect('customer:customer_login')


class UpdatePatientDetailAPI(GenericAPIView):

    def post(self, request):
        data = request.data
        patient_through_adhar = None

        patient = Patient.objects.get(slug=data['slug'])

        try:
            patient_through_adhar = Patient.objects.get(adhar=data['adhar'])
        except:
            pass

        if patient_through_adhar != None:
            if patient_through_adhar.slug != patient.slug:
                return Response({'update': False})
        
        patient.name = request.POST.get('name', patient.name)
        patient.gender = request.POST.get('gender', patient.gender)
        patient.p_mobile = request.POST.get('p_mobile', patient.p_mobile)
        patient.s_mobile = request.POST.get('s_mobile', patient.s_mobile)
        patient.adhar = request.POST.get('adhar', patient.adhar)
        patient.dob = request.POST.get('dob', patient.dob)
        patient.status = request.POST.get('status', patient.status)
        patient.bed = request.POST.get('bed', patient.bed)
        patient.save()

        patient_serialized_data = PatientSerializer(patient)
        return Response({'patient': patient_serialized_data.data, 'update': True})        


class TempAddPatientAPI(GenericAPIView):

    def create_noticication_(self, hospital_id, user, booking_obj, bed_type):
        notification_body = f'{user.username} requested for a {bed_type} bed.'
        notification = Notification.objects.create(hospital_id=hospital_id, notification_body=notification_body, booking_request=booking_obj)

    def update_booking_obj(self, adhar, hospital):
        booking_obj = BookingRequest.objects.get(adhar=adhar)   # get booking_request obj
        booking_obj.to_hospital.add(hospital)   # add hospital to bookking_request obj
        return booking_obj
    
    def create_activity(self, user, bed_type, patient_name, hospital_name):
        text = f'You ({user.username}) send a {bed_type} bed request for patient {patient_name} to {hospital_name}'
        Activity.objects.create(user=user, text=text)
    
    def check_patient_details(self, data, temp_patient):
        message = None
        if data['name'] != temp_patient.name:
            message = f'Patient details not match. Please enter correct details.'
            return False, message

        if data['gender'] != temp_patient.gender:
            message = f'Patient details not match. Please enter correct details.'
            return False, message
        
        # if data['dob'] != temp_patient.dob:
        #     print('dob')
        #     return False

        if data['bed'] != temp_patient.bed:
            message = f'Bed type does not match with your previous request for patient {data["name"]}'
            return False, message
        return True, None

    def post(self, request):
        data = request.data
        user = request.user
        hospital = Hospital.objects.get(slug=data['hospital'])
        temp_patient = None
        
        try:
            temp_patient = TempPatientDetails.objects.get(adhar=data['adhar'])
        except:
            pass
        
        if temp_patient != None:

            ack, message = self.check_patient_details(data, temp_patient)
            if ack!=True:
                return Response({'added': False, 'message': message})

            hospitals_of_temp_patient = temp_patient.hospital.all()

            if len(hospitals_of_temp_patient) >= 2:
                return Response({'added': False, 'message': 'You can\'t apply more than two beds for each patient.'})

            for i in hospitals_of_temp_patient:
                if i.slug == data['hospital']:
                    return Response({'added': False, 'message': 'You can\'t apply more than one bed for one patient at the same hospital. You can try in another hospital.'})

            temp_patient.hospital.add(hospital)
            booking_obj = self.update_booking_obj(data['adhar'], hospital)
            self.create_noticication_(hospital.hospital_id, user, booking_obj, data['bed'])   # create new notification
            self.create_activity(user, data['bed'], data['name'], hospital.name)
        else:
            temp_patient = TempPatientDetails.objects.create(reference_user=user, name=data['name'], gender=data['gender'], p_mobile=data['p_mobile'], s_mobile=data['s_mobile'], adhar=data['adhar'], dob=data['dob'], bed=data['bed'])
            temp_patient.hospital.add(hospital) # add hospital to temp_patient obj
            booking_obj =self.update_booking_obj(data['adhar'], hospital)
            self.create_noticication_(hospital.hospital_id, user, booking_obj, data['bed'])   # create new notification
            self.create_activity(user, data['bed'], data['name'], hospital.name)

        if temp_patient:
            return Response({'added': True, 'hospital_id': hospital.hospital_id, "message": 'Request send for a bed.'})
        return Response({'added': False})



class HospitalSearchAPI(ListAPIView):

    serializer_class = HospitalSerializer
    queryset = Hospital.objects.filter(Q(word_bed__gt=0) | Q(icu_bed__gt=0))
    filter_backends =[SearchFilter]
    search_fields = ['name', 'city', 'state', 'address']




