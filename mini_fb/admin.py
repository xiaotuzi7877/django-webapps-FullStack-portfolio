# File: admin.py
# Author: Li Ziyang (miclilzy@bu.edu), 02/21/2025
# Description: This file registers the Profile model with the Django admin interface,
# allowing administrators to manage user profiles through the Django admin panel.
from django.contrib import admin

# Register your models here.
from .models import Profile, StatusMessage, Image, StatusImage, Friend

# Register the Profile model to make it accessible in the Django admin interface.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(StatusImage)
admin.site.register(Friend)