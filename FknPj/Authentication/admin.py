from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profile_pic', 'mobile_number')

admin.site.register( CustomUser) 