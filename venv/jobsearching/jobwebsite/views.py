from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import Job, Profile
from . forms import UpdateProfile
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def home(request):
    return render(request, "jobwebsite/home.html")


def profile(request):
    user = None
    profile = None
    if request.user.is_authenticated:
        user = request.user
        try:
            Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            Profile.objects.create(user=user)
        profile = Profile.objects.get(user=user)
        print(profile)
        if request.method == "POST":
            form = UpdateProfile(request.POST, request.FILES,
                                 instance=request.user.profile)
            if form.is_valid():
                profile.username = form.cleaned_data["username"]
                profile.first_name = form.cleaned_data["first_name"]
                profile.last_name = form.cleaned_data["last_name"]
                profile.age = form.cleaned_data["age"]
                profile.email = form.cleaned_data["email"]
                profile.birthdate = form.cleaned_data["birthdate"]
                profile.save()
        else:
            form = UpdateProfile(instance=request.user.profile)

        return render(request, "jobwebsite/profile.html", {'form': form})
    else:
        return redirect("/signup/")


def search(request):
    if request.user.is_authenticated:
        return render(request, "jobwebsite/search.html")
    else:
        return HttpResponseRedirect("/signup/")
