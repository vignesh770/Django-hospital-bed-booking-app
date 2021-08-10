from django.shortcuts import render, redirect
from django.views import View

from .models import *
from bookpatient.models import Notification
from customer.views import logged_in as user_logged_in


def logged_in(request):
    user = request.user

    if user.is_authenticated == True and user.admin == False and user.is_customer == False and user.is_authority == True:
        return True
    else:
        return False


class HospitalRegistrationView(View):
    template_name = 'hospital/hospital-registration.html'

    def get(self, request):
        return render(request, self.template_name)


class HospitalLoginView(View):
    template_name = 'hospital/hospital-authority-login.html'

    def get(self, request):
        if logged_in(request):
            return redirect('hospital:dashboard')
        else:
            return render(request, self.template_name)


class HospitalDashboardView(View):
    template_name = 'hospital/hospital-dashboard.html'
    
    def get(self, request):
        user = request.user

        if logged_in(request):
            hospital = Hospital.objects.get(user=user.pk)
            notifications = Notification.objects.order_by('-timestamp').filter(hospital_id__iexact=hospital.hospital_id)
            return render(request, self.template_name, {'hospital': hospital, 'notifications': notifications})
        else:
            return redirect('hospital:login')


class HospitalDetailView(View):
    template_name = 'hospital/inner-hospital.html'
    page_not_found = 'page-not-found.html'

    def get_object(self, slug):
        try:
            hospital = Hospital.objects.get(slug=slug)
            return hospital
        except:
            return None    

    def get(self, request, slug):

        if self.get_object(slug) != None:
            hospital = self.get_object(slug)

            if user_logged_in(request):                
                return render(request, self.template_name, {
                    'hospital': hospital,
                })
            else:
                return redirect('customer:customer_login')
        else:
            return render(request, self.page_not_found, {'info': 'Invalid hospital slug'})


