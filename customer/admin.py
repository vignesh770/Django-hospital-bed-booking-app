from django.contrib import admin

from customer.models import Patient


class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'adhar', 'status', 'created_at']
    list_display_links = ['name']
    list_filter = ['status']
    list_per_page = 50
    search_fields = ['name', 'adhar']
admin.site.register(Patient, PatientAdmin)

