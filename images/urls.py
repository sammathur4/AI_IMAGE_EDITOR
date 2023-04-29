from django.urls import path
from .views import *

urlpatterns = [
    path('remove_background/', image_upload, name='image_upload'),
]




