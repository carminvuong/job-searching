from django import forms


class UpdateProfile(forms.Form):
    fullname = forms.CharField(max_length="100", required=False)
    age = forms.IntegerField(required=False)
    height = forms.IntegerField(required=False)
    weight = forms.IntegerField(required=False)
