from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import Job, Profile
from careerjet_api_client import CareerjetAPIClient
from .forms import UserForm, UpdateProfile, JobForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .webscraper import getDescription, getSeeMore
from django.template import *
import json


# Create your views here.

fav = []

def home(request):
    form = JobForm()
    return render(request, "jobwebsite/home.html", {'form': form})


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = UpdateProfile(request.POST, instance=request.user.profile)

            if profile_form.is_valid() and user_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                # return redirect(to='jobwebsite\profile.html')
        else:
            user_form = UserForm(instance=request.user)
            profile_form = UpdateProfile(instance=request.user.profile)

        return render(request=request, template_name=r"jobwebsite\profile.html", context={"user": request.user, 'user_form': user_form, 'profile_form': profile_form})
    else:
        return HttpResponseRedirect("/login/")

def support(request):
    return render(request, "jobwebsite/support.html")

def findJob(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = JobForm(request.POST)
            if request.POST.get("favorite"):

                object_id = request.POST["favorite"]
                job_object = Job.objects.get(id=object_id)
                job_object.favorite = True
                fav.append(job_object)
                return HttpResponseRedirect('/favorites/')
            if request.POST.get("moreInfo"):
                object_id = request.POST["moreInfo"]
                job_object = Job.objects.get(id=object_id)
                description = str(getDescription(job_object.url))
                description = description.replace("<br/>", "")
                description = description.replace("<li>", " \n")
                description = description.replace("</li>", "")
                description = description.replace("<b>", " ")
                description = description.replace("</b>", " ")
                job_object.fullDescription = description

                return render(request, "jobwebsite/moreInfo.html/", {"job": job_object})

            elif form.is_valid():
                lc = form.cleaned_data["location"]
                kw = form.cleaned_data["keywords"]
                cj = CareerjetAPIClient("en_US")
                result_json = cj.search({
                    'location': lc,
                    'keywords': kw,
                    'affid': '213e213hd12344552',
                    'user_ip': '11.22.33.44',
                    'url': 'https://www.netflix.com/browse',
                    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
                })
                json_object = json.dumps(result_json, indent=4)
                with open("jobs.json", "w") as outfile:
                    outfile.write(json_object)
                    outfile.close()
                jobs = result_json["jobs"]
                print(jobs)
                all_jobs = []
                kw_list = "+".join(kw.split(" "))
                lc_list = "+".join(lc.split(" "))
                count = 0
                user = request.user
                for i in jobs:
                    job = Job()
                    job.user = user
                    job.title = i["title"]
                    job.company = i["company"]
                    job.salary = i["salary"]
                    job.location = i["locations"]
                    job.url = i["url"]
                    descriptions = getSeeMore(job.url)
                    job.description = descriptions[0]
                    # job.description = "poopy head"
                    print("JOB DESCRIPTION: "+job.description + "count :"+str(count))
                    count += 1

                    all_jobs.append(job)
                    job.save()
                return render(request, 'jobwebsite/results.html/', {"jobs": all_jobs,  "a": kw})
        else:
            form = JobForm()
        return render(request, 'jobwebsite/findJob.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")
