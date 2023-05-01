from django import forms
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django import forms
from .models import Image





class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('image',)
