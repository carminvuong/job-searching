from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from . models import Job, Profile
from careerjet_api import CareerjetAPIClient
from .forms import UserForm, UpdateProfile, JobForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from .webscraper import getDescription, getSeeMore
from django.template import *
import json
import os
from datetime import date

all_jobs = []
kw = ""
lc = ""

def file_is_empty(path):
    return os.stat(path).st_size == 0

def home(request):
    form = JobForm()
    return render(request, "jobwebsite/home.html", {'form': form})


def profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user = request.user
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = UpdateProfile(request.POST, instance=request.user.profile)
            favorites = user.profile.get_fave()
            favs = list(favorites.values())
            for i in range(0,len(favs)):
                favs[i] = globals()[favs[i]]
            if profile_form.is_valid() and user_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect(to='/profile/', context={"user": request.user, 'user_form': user_form, 'profile_form': profile_form,"favs":favs})
        else:
            user = request.user
            all_jobs = []
            user_form = UserForm(instance=request.user)
            profile_form = UpdateProfile(instance=request.user.profile)
            favorites = user.profile.get_fave()
            favs = list(favorites.values())
            for i in range(0,len(favs)):
                all_jobs.append(Job.objects.get(id=favs[i]))
        return render(request=request, template_name=r"jobwebsite/profile.html", context={"user": request.user, 'user_form': user_form, 'profile_form': profile_form,"favs":all_jobs})
    else:
        return HttpResponseRedirect("/login/")

def support(request):
    return render(request, "jobwebsite/support.html")

def findJob(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = JobForm(request.POST)
            if form.is_valid():
                lc = form.cleaned_data["location"].lower()
                kw = form.cleaned_data["keywords"].lower()
                cj = CareerjetAPIClient("en_US")
                #Returns json (dictionary)
                result_json = cj.search({
                    'location': lc,
                    'keywords': kw,
                    'affid': '213e213hd12344552',
                    'user_ip': '11.22.33.44',
                    'url': 'https://www.moomoo.io',
                    'user_agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
                })
                #Checking if location is 2+ words
                if len(lc.split(" ")) > 1:
                    lst = lc.split(" ")
                    lc = "_".join(lst)
                if len(kw.split(" ")) > 1:
                    lst = kw.split(" ")
                    kw = "_".join(lst)
                #Storing result_json dictionary in new dictionary
                #Key is location+keyword
                #Changes json to string
                json_object = json.dumps(result_json, indent=4)
                #If file is not empty
                if not(file_is_empty("jobs.json")):
                    f = open("jobs.json")
                    #Changes string to json
                    data = json.load(f)
                    f.close()
                    #Checks if keyword and location are same as inputted kw and lc
                    if f"{lc} {kw}" in data.keys():
                        all_jobs = []
                        dictionary = data[f"{lc} {kw}"]
                        #foundJobs is list of dictionaries (jobs)
                        foundJobs = dictionary["jobs"]
                        #Creates Job object with info from dictionaries; n is the dict
                        for n in foundJobs: 
                            job = Job()
                            job.user = request.user 
                            job.title = n["title"]
                            job.company = n["company"]
                            job.salary = n["salary"]
                            job.location = n["locations"]
                            job.url = n["url"]
                            description = n["description"]
                            description = description.replace("<br/>", "")
                            description = description.replace("<li>", " \n")
                            description = description.replace("</li>", "")
                            description = description.replace("<b>", " ")
                            description = description.replace("</b>", " ")
                            description = description.replace(".", ". ")
                            description = description.replace(":", ": ")
                            description = description.replace(",", ", ")
                            job.description = description
                            all_jobs.append(job)
                            job.save()
                            kw = " ".join(kw.split("_"))
                            lc = " ".join(lc.split("_"))
                        return HttpResponseRedirect("/results/")
                    #Writing api returned json into file
                    #If different inputs then write a description for each job
                    else:
                        data[f"{lc} {kw}"] = result_json
                        for j in data[f"{lc} {kw}"]["jobs"]:
                            description = getDescription(j["url"])
                            if description:
                                j["description"] = description[0]
                            else:
                                j["description"] = ""
                    jobs = data[f"{lc} {kw}"]["jobs"]
                    all_jobs = []
                    user = request.user 
                    for i in jobs: 
                        job = Job()
                        job.user = user 
                        job.title = i["title"]
                        job.company = i["company"]
                        job.salary = i["salary"]
                        job.location = i["locations"]
                        job.url = i["url"]
                        job.description = i["description"]
                        all_jobs.append(job)
                        # user.profile.add_fav(job)
                        job.save()
                        with open("jobs.json", "w") as outfile:
                            outfile.write(json.dumps(data,indent=4))
                            outfile.close()
                        kw = " ".join(kw.split("_"))
                        lc = " ".join(lc.split("_"))
                    return HttpResponseRedirect('results')
                else:
                    result = {}
                    result[f"{lc} {kw}"] = result_json
                    result_json = result
                    jobs = result_json[f"{lc} {kw}"]["jobs"]
                    all_jobs = []
                    user = request.user 
                    for i in jobs: 
                        job = Job()
                        job.user = user 
                        job.title = i["title"]
                        job.company = i["company"]
                        job.salary = i["salary"]
                        job.location = i["locations"]
                        job.url = i["url"]
                        description = getDescription(job.url)
                        if not(description):
                            description = [""]
                        job.description = description[0]
                        all_jobs.append(job)
                        print(job)
                        job.save()
                    with open("jobs.json", "w") as outfile:
                        outfile.write(json.dumps(result_json,indent=4))
                        outfile.close()
                    kw = " ".join(kw.split("_"))
                    lc = " ".join(lc.split("_"))
                    return HttpResponseRedirect('/results/')
        else:
            form = JobForm()
        return render(request, 'jobwebsite/findJob.html', {'form': form})
    else:
        return HttpResponseRedirect("/login/")
    

def results(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if request.POST.get("favorite"):
                profile = request.user.profile
                object_id = request.POST["favorite"]
                job_object = Job.objects.get(id=object_id)
                job_object.favorite = True 
                profile.add_fav({profile.favCount:job_object.id})
                print("FAVORITED: "+profile.favorites)
                request.user.save()
                profile.save()
            print("All Jobs: "+all_jobs)
            return render(request, 'jobwebsite/results.html/', {"jobs": all_jobs,  "kw":" ".join(kw.split("_")),"lc":" ".join(lc.split("_"))})
        else:
            return render(request, 'jobwebsite/results.html/', {"jobs": all_jobs,  "kw":" ".join(kw.split("_")),"lc":" ".join(lc.split("_"))})    
    else:
        return HttpResponseRedirect("/login/")