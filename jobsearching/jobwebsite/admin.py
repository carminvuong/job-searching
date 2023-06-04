from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# Register your models here.
admin.site.register(Profile)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "profile"


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
