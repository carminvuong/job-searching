from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import Job, Profile
from . forms import UserForm, UpdateProfile, JobForm
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def home(request):
    form = JobForm()
    return render(request, "jobwebsite/home.html", {'form': form})


def profile(request):
    if request.user.is_authenticated:
        user_form = UserForm(instance=request.user)
        profile_form = UpdateProfile(instance=request.user.profile)

        return render(request=request, template_name=r"jobwebsite\profile.html", context={"user": request.user, "user_form": user_form, "profile_form": profile_form})
    else:
        return HttpResponseRedirect("/login/")


def search(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            return render(request, "jobwebsite/search.html")
    else:
        return HttpResponseRedirect("/login/")


def findJob(request):
    if request.user.is_authenticated:

        return render(request, "jobwebsite/findJob.html")
    else:
        return HttpResponseRedirect("/login/")
