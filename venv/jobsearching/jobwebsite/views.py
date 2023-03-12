from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "jobwebsite/home.html")

def profile(request):
    return render(request, "jobwebsite/profile.html")