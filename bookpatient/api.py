from hospital.models import Hospital
from django.core.checks import messages
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import BookingRequest, ConformRequest, CancelRequest, Notification, Activity, TempPatientDetails
from customer.models import Patient
from userapp.models import Account
from OnlineBedBookingSystem.custom import send_mail_to_customer


class BookBedAPI(GenericAPIView):

    def temp_patient_to_ptient(self, booking_obj, user):
        hospital_obj = Hospital.objects.get(user=user)
        temp_patient = TempPatientDetails.objects.get(adhar=booking_obj.adhar)
        patient = None

        patient = Patient.objects.create(
            reference_user=booking_obj.from_user, 
            hospital=hospital_obj, 
            name=temp_patient.name, 
            gender=temp_patient.gender,
            p_mobile=temp_patient.p_mobile, 
            s_mobile=temp_patient.s_mobile,
            status=temp_patient.status,
            adhar=temp_patient.adhar,
            dob=temp_patient.dob,
            bed=temp_patient.bed
        )
        temp_patient.delete()   # delete temp patient
        return patient

    def post(self, request):
        data = request.data
        user = request.user
        action = data['action']
        notification_id = data['id']

        notification = Notification.objects.get(id=notification_id)
        booking_obj = BookingRequest.objects.get(id=notification.booking_request.id)

        if action == 'confirm':
            
            # try:
            #     ConformRequest.objects.get(request=booking_obj.id)
            #     return Response({'status': False, 'message': 'This requested is already confirmed by another hospital. Please refresh your page.'})
            # except:
            #     pass

            created = self.temp_patient_to_ptient(booking_obj, user)
            if created is not None:
                confirm_request = ConformRequest.objects.create(request=booking_obj, user=user) # create confirm request

                notifications = Notification.objects.filter(booking_request=booking_obj.id)
                for notification in notifications:
                    notification.show = False
                    notification.save()

                # create new activity for user
                message = f'You ({user.username}) added one new patient, referenced user "{booking_obj.from_user.username}".'
                Activity.objects.create(user=user, text=message)
                
                # send mail
                hospital_obj = Hospital.objects.get(user=user)
                patient = Patient.objects.get(adhar=booking_obj.adhar)
                message_body = f'{hospital_obj.name} confirm your bed request for the patient {patient.name}.'
                send_mail_to_customer(subject='Confirmation mail', message=message_body, email=booking_obj.from_user.email)

                return Response({'status': True, 'message': message})
        
        elif action == 'cancel':
            cancel_request = CancelRequest.objects.create(request=booking_obj, user=user)
            notification.show = False
            notification.save()
            
            message = f'You ({user.username}) cancel one request, referenced user "{booking_obj.from_user.username}".'
            Activity.objects.create(user=user, text=message)

            # send mail
            hospital_obj = Hospital.objects.get(user=user)
            patient = TempPatientDetails.objects.get(adhar=booking_obj.adhar)
            message_body = f'{hospital_obj.name} cancel your bed request for the patient {patient.name}. You can apply in another hospital.'
            send_mail_to_customer(subject='Cancellation mail', message=message_body, email=booking_obj.from_user.email)

            temp_patient = TempPatientDetails.objects.get(adhar=booking_obj.adhar)
            temp_patient.delete()   # delete temp patient

            return Response({'status': True, 'message': message})

        return Response({'status': False})

