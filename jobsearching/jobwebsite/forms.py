from django import forms
from .models import Profile


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
