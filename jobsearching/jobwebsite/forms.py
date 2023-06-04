from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class UpdateProfile(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control-file'}))
    username = forms.CharField(max_length="1000", required=False)
    first_name = forms.CharField(max_length='1000', required=False)
    last_name = forms.CharField(max_length='1000', required=False)
    age = forms.IntegerField(required=False)
    email = forms.EmailField(required=False)
    birthdate = forms.DateField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'username', 'first_name',
                  'last_name', 'age', 'email', 'birthdate']
