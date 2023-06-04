from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import Job, Profile
from . forms import UserForm, UpdateProfile
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def home(request):
    return render(request, "jobwebsite/home.html")


def profile(request):
    if request.user.is_authenticated:
        user_form = UserForm(instance=request.user)
        profile_form = UpdateProfile(instance=request.user.profile)

        return render(request=request, template_name=r"jobwebsite\profile.html", context={"user": request.user, "user_form": user_form, "profile_form": profile_form})
    else:
        return HttpResponseRedirect("/signup/")


def search(request):
    if request.user.is_authenticated:
        return render(request, "jobwebsite/search.html")
    else:
        return HttpResponseRedirect("/signup/")
