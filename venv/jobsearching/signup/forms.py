from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from bootstrap_datepicker_plus.widgets import (DatePickerInput, DateTimePickerInput,
                                               MonthPickerInput,
                                               TimePickerInput,
                                               YearPickerInput,)


class SignupForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=1000)
    last_name = forms.CharField(max_length=1000)
    birth_date = forms.DateField(widget=DatePickerInput(
        options={
            "format": "mm/dd/yyyy",
            "autoclose": True
        }
    ))

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "start_date",
                  "end_date",
                  "start_time",
                  "end_time",
                  "start_datetime",
                  "end_datetime",
                  "start_month",
                  "end_month",
                  "start_year",
                  "end_year",
                  "email", "password1", "password2"]
        widgets = {
            "start_date": DatePickerInput(options={"format": "MM/DD/YYYY"}),
            "end_date": DatePickerInput(
                options={"format": "MM/DD/YYYY"}, range_from="start_date"
            ),
            "start_datetime": DateTimePickerInput(),
            "end_datetime": DateTimePickerInput(range_from="start_datetime"),
            "start_time": TimePickerInput(),
            "end_time": TimePickerInput(range_from="start_time"),
            "start_month": MonthPickerInput(),
            "end_month": MonthPickerInput(range_from="start_month"),
            "start_year": YearPickerInput().start_of("deprecated! do not use start_of"),
            "end_year": YearPickerInput().end_of("deprecated! do not use end_of"),
        }

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
