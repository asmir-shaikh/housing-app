from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea

from .models import Housing


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class SubmitHousing(forms.ModelForm):
    class Meta:
        model = Housing
        fields = ['title', 'rent','location', 'bed','bath', 'footage',  'link', 'imgadd','description']
        widgets = {
            'description': Textarea(attrs={'cols': 19, 'rows': 5}),
        }

    # Source for form field aliasing: https://stackoverflow.com/questions/2070377/django-modelform-adding-an-alias-to-a-field
    def __init__(self, *args, **kwargs):
        super(SubmitHousing, self).__init__(*args, **kwargs)
        self.fields['imgadd'].label = 'Cover Image URL'
        self.fields['link'].label = 'Property Website Link'
        self.fields['footage'].label = 'Property Square Footage'
        self.fields['rent'].label = 'Rent per Month'


