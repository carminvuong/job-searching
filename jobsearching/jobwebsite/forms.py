from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name')


class UpdateProfile(forms.ModelForm):
    email = forms.EmailField(required=False)
    username = forms.CharField(max_length="1000", required=False)
    first_name = forms.CharField(max_length='1000', required=False)
    last_name = forms.CharField(max_length='1000', required=False)
    age = forms.IntegerField(required=False)
    birthdate = forms.DateField(required=False)

    class Meta:
        model = Profile
        fields = ['email', 'username', 'first_name',
                  'last_name', 'age', 'birthdate']


class JobForm(forms.Form):
    keywords = forms.CharField(label="keywords")
    location = forms.CharField(label="location")
