from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import (DatePickerInput, DateTimePickerInput,
                                               MonthPickerInput,
                                               TimePickerInput,
                                               YearPickerInput,
                                               )


class SignupForm(UserCreationForm):

    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'style': 'width: 300px;', 'class': 'form-control'}))
    first_name = forms.CharField(max_length=1000, widget=forms.TextInput(
        attrs={'placeholder': 'First Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    last_name = forms.CharField(max_length=1000, widget=forms.TextInput(
        attrs={'placeholder': 'Last Name', 'style': 'width: 300px;', 'class': 'form-control'}))
    birth_date = forms.DateField(
        label="Birthday", widget=DatePickerInput())

    class Meta:
        model = User
        fields = ["email", "username", "first_name", "last_name", "birth_date",
                  "password1", "password2"]

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.birth_date = self.cleaned_data['birth_date']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'Username', 'required': 'required', 'style': 'width: 300px;'}
        self.fields['password1'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'Password', 'required': 'required', 'style': 'width: 300px;'}
        self.fields['password2'].widget.attrs = {
            'class': 'form-control', 'placeholder': 'Confirm Password', 'required': 'required', 'style': 'width: 300px;'}
        self.fields['birth_date'].widget.attrs = {
            'required': 'required', 'placeholder': 'YYYY-MM-DD'}
