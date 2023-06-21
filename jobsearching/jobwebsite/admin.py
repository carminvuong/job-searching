from django.contrib import admin
from .models import Profile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Profile

# Register your models here.
admin.site.register(Profile)

