""" Registering Users models """
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, OTP


class CustomUserAdmin(UserAdmin):
    """ Admin for CustomUser model """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("username", "first_name", "last_name", "email", "is_verified",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "password", "is_verified",)}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)
