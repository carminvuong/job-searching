from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name',
                  'last_name')

class UpdateProfile(forms.ModelForm):
    email = forms.EmailField(required=False, 
                             widget=forms.TextInput(attrs={'class': 'form-control small mb-1'}))
    username = forms.CharField(max_length="1000", required=False, widget=forms.TextInput(attrs={'class': 'form-control small mb-1'}))
    first_name = forms.CharField(max_length='1000', required=False, widget=forms.TextInput(attrs={'class': 'form-control small mb-1'}))
    last_name = forms.CharField(max_length='1000', required=False, widget=forms.TextInput(attrs={'class': 'form-control small mb-1'}))
    age = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    birthdate = forms.DateField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['email', 'username', 'first_name',
                  'last_name', 'age', 'birthdate']


class JobForm(forms.Form):
    keywords = forms.CharField(max_length="1000", required=True, widget=forms.TextInput(attrs={'placeholder': 'Garden', 'style': 'width: 250px;', 'class': 'form-control-lg mb-1'}))
    location = forms.CharField(max_length="1000", required=True, widget=forms.TextInput(attrs={'placeholder': 'California', 'style': 'width: 250px;', 'class': 'form-control-lg mb-1'}))
