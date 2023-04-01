from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import Job, Profile
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def home(request):
    return render(request, "jobwebsite/home.html")


def profile(request):
    user = None
    profile = None
    complete = False
    if request.user.is_authenticated:
        user = request.user
        try:
            Profile.objects.get(user=user)
        except ObjectDoesNotExist:
            Profile.objects.create(user=user)

        profile = Profile.objects.get(user=user)
        if profile.fullname != None and profile.age != None and profile.height != None and profile.weight != None:
            complete = True
        if request.method == "POST":
            form = UpdateProfile(request.POST)
            if form.is_valid():
                profile.fullname = form.cleaned_data["fullname"]
                profile.age = form.cleaned_data["age"]
                profile.height = form.cleaned_data["height"]
                profile.weight = form.cleaned_data["weight"]
                complete = True
                profile.save()
            return render(request, "jobwebsite/profile.html")
    else:
        return redirect("/signup/")


def search(request):
    if request.user.is_authenticated:
        return render(request, "jobwebsite/search.html")
    else:
        return HttpResponseRedirect("/signup/")
