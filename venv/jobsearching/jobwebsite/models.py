from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import date
from PIL import Image


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
    avatar = models.ImageField(
        default='Cat03.jpg', upload_to='images')
    username = models.CharField(max_length=3000, default="")
    first_name = models.CharField(max_length=3000, default="")
    last_name = models.CharField(max_length=3000, default="")
    age = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)],
                                      default=18)
    email = models.EmailField(default="")
    birthdate = models.DateField(default=date.today())

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(
            'C:\\Users\\JackJ\\OneDrive\\Desktop\\job-searching\\venv\\jobsearching\\jobwebsite\\static\\images\\Cat03.jpg')

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(
                'C:\\Users\\JackJ\\OneDrive\\Desktop\\job-searching\\venv\\jobsearching\\jobwebsite\\static\\images\\Cat03.jpg')

    def __str__(self):
        # show how we want it to be displayed
        return f'{self.user.username} Profile'
