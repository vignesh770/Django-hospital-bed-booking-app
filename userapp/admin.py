from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

class AccountAdmin(UserAdmin):
    list_display = ['username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_customer', 'is_authority']
    list_per_page = 30
    search_fields = ['username', 'first_name', 'email']
    readonly_fields = ['last_login', 'date_joined']
    filter_horizontal = ()
    list_filter = ['is_customer', 'is_authority']
    fieldsets = ()

admin.site.register(Account, AccountAdmin)

