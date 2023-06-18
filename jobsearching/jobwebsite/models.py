from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from PIL import Image
import json


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="")
    company = models.CharField(max_length=200, default="")
    salary = models.CharField(max_length=200, default="")
    location = models.CharField(max_length=200, default="")
    url = models.CharField(max_length=1000, default="")
    description = models.CharField(max_length=5000, default="")
    fullDescription = models.CharField(
        max_length=50000, default="")
    favorite = models.BooleanField(default=False)


class Profile(models.Model):
    # Delete profile when user is deleted
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(100)],
                                      default=18)
    birthdate = models.DateField(default=date.today())
    favorites = models.CharField(max_length = 1000000,default="{}")
    favCount = models.IntegerField(default=0)

    def add_fav(self, fav):
        dictFav = json.loads(self.favorites)
        dictFav.update(fav)
        self.favorites = json.dumps(dictFav)
        self.favCount = self.favCount + 1
        
    def get_fave(self):
        return json.loads(self.favorites)
    def save(self, *args, **kwargs):
        super().save()

    def __str__(self):
        # show how we want it to be displayed
        return f'{self.user.username} Profile'
