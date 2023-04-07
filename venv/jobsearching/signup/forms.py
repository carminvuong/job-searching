from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import (DatePickerInput, DateTimePickerInput,
                                               MonthPickerInput,
                                               TimePickerInput,
                                               YearPickerInput,)


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length='1000')
    email = forms.EmailField(help_text='A valid email address, please.')
    first_name = forms.CharField(max_length=1000)
    last_name = forms.CharField(max_length=1000)
    birth_date = forms.DateField(
        label="Date", widget=DatePickerInput(), initial="2021-12-13")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "birth_date",
                  "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.password1 = self.cleaned_data['password1']
        user.password2 = self.cleaned_data['password2']

        if commit:
            user.save()
        return user
