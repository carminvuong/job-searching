from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import (DatePickerInput, DateTimePickerInput,
                                               MonthPickerInput,
                                               TimePickerInput,
                                               YearPickerInput,
                                               )
from django.forms import EmailInput, TextInput, PasswordInput


class SignupForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=1000, widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=1000, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    birth_date = forms.DateField(
        label="Date", widget=DatePickerInput(), initial="2021-12-13")
    age = forms.IntegerField(widget=forms.TextInput(
        attrs={'min': 16, 'max': 100, 'value': 18, 'type': 'number', 'style': 'max-width: 5em'}))
    # password1 = forms.CharField(max_length=1000, widget=forms.PasswordInput(
    #    attrs={'placeholder': 'Password1', 'style': 'width: 300px;', 'class': 'form-control'}))
    # password2 = forms.CharField(max_length=1000, widget=forms.PasswordInput(
    #    attrs={'placeholder': 'Password2', 'style': 'width: 300px;', 'class': 'form-control'}))

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "age", "birth_date",
                  "password1", "password2"]

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.age = self.cleaned_data['age']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user
