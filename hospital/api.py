from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, redirect

from .models import *
from customer.models import *
from customer.serializers import *
from .serializers import *
from userapp.serializers import AccountRegisterSerializer
from bookpatient.models import *


class CreateHospital(GenericAPIView):
    
    def post(self, request):
        data = request.data

        context = {
            'username': data['username'],
            'password': data['password'],
            'email': data['email'],
            'is_authority': True
        }

        user_serializer = AccountRegisterSerializer(data=context)
        if user_serializer.is_valid():
            user_serializer.save()
        else:
            return Response(user_serializer.errors)

        user = Account.objects.get(username=user_serializer.data['username'])  # get user obj

        data._mutable = True
        data['user'] = user.pk      # change user value to a user_object_id

        serializer = HospitalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return Response({'user_deatils': serializer.data, 'login': True})
        return Response(serializer.errors)
  

class HospitalAuthorityLoginAPI(GenericAPIView):

    def post(self, request):
        data = request.data
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            return Response({'login': True})
        return Response({'error': 'Incorrect login credentials.', 'login': False})


class HospitalAuthorityLogoutAPI(GenericAPIView):

    def get(self, request):
        user = request.user
        if user:
            logout(request)
        return redirect('hospital:login')


class PatientListView(GenericAPIView):
    serializer_class = PatientSerializer

    def get(self, request, status):
        user = request.user
        hospital = None
        try:
            hospital = Hospital.objects.get(user=user)
        except:
            pass

        if hospital != None:
            word_bed = hospital.word_bed
            icu_bed = hospital.icu_bed
            if status == 'All':
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(hospital=hospital.pk))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status, 'word_bed': word_bed, 'icu_bed': icu_bed})
            else:
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(hospital=hospital.pk) & Q(status__iexact=status))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status, 'word_bed': word_bed, 'icu_bed': icu_bed})
        else:
            if status == 'All':
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(reference_user=user.pk))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status})
            else:
                patient_queryset = Patient.objects.order_by('-update_at').filter(Q(reference_user=user.pk) & Q(status__iexact=status))
                patient_serialized_data = self.serializer_class(patient_queryset, many=True)
                return Response({'patients': patient_serialized_data.data, 'status': status})


class UpdateBedAPI(GenericAPIView):
    def post(self, request):
        data = request.data
        hospital_obj = Hospital.objects.get(user=request.user)

        if data['bed_type'] == 'word_bed':
            hospital_obj.word_bed = data['bed']
            hospital_obj.save()
        elif data['bed_type'] == 'icu_bed':
            hospital_obj.icu_bed = data['bed']
            hospital_obj.save()
        return Response({'word_bed': hospital_obj.word_bed, 'icu_bed': hospital_obj.icu_bed})


class PatientDetailView(GenericAPIView):
    patient_view_for_hospital = 'hospital/patient-view.html'
    page_not_found = 'page-not-found.html'
    patient_view_for_customer = 'customer/patient-view.html'

    def get(self, request, slug):
        
        user = request.user

        if user.is_authenticated and user.is_customer:
            try:
                patient_obj = Patient.objects.get(slug=slug, reference_user=user.pk)
                patient_serialized_data = PatientSerializer(patient_obj, many=False)
                return render(request, self.patient_view_for_customer, {'patient': patient_serialized_data.data})
            except:
                return render(request, self.page_not_found, {'info': 'Patient not found.'})
        
        elif user.is_authenticated and user.is_authority:
            hospital = Hospital.objects.get(user=user.pk)
            try:
                patient_obj = Patient.objects.get(slug=slug, hospital=hospital.pk)
                patient_serialized_data = PatientSerializer(patient_obj, many=False)
                return render(request, self.patient_view_for_hospital, {'patient': patient_serialized_data.data})
            except:
                return render(request, self.page_not_found, {'info': 'Patient not found.'})



class AddPatientAPI(GenericAPIView):

    def post(self, request):
        data = request.data
        user = request.user
    
        hospital = Hospital.objects.get(user=user)
        patient = Patient.objects.create(reference_user=user, hospital=hospital, name=data['name'], gender=data['gender'], p_mobile=data['p_mobile'], s_mobile=data['s_mobile'], adhar=data['adhar'], dob=data['dob'], bed=data['bed'])
        if patient:
            text = f'You ({user.username}) added a new patient {data["name"]}.'
            Activity.objects.create(user=user, text=text)
            return Response({'added': True})
        return Response({'added': False})
        


class HospitalBedDetalAPI(GenericAPIView):

    def get(self, request, slug):
        hospital = Hospital.objects.get(slug=slug)

        patient_word_bed = Patient.objects.filter(Q(hospital=hospital.pk) & Q(bed='word')).count()
        patient_icu_bed = Patient.objects.filter(Q(hospital=hospital.pk) & Q(bed='icu')).count()

        temp_patient_word_bed = TempPatientDetails.objects.filter(Q(hospital=hospital.pk) & Q(bed='word')).count()
        temp_patient_icu_bed = TempPatientDetails.objects.filter(Q(hospital=hospital.pk) & Q(bed='icu')).count()

        availabel_word_bed = hospital.word_bed - patient_word_bed
        availabel_icu_bed = hospital.icu_bed - patient_icu_bed

        data = {
            'available_word_bed': availabel_word_bed,
            'available_icu_bed': availabel_icu_bed,
            'waiting_word_bed': temp_patient_word_bed,
            'waiting_icu_bed': temp_patient_icu_bed
        }
        return Response(data)


