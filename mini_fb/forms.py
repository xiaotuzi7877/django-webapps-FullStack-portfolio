"""
file: forms.py

This module defines the forms used in the Mini Facebook application, 
including the CreateProfileForm to allow users to create new profiles.

Author: Li Ziyang (miclilzy@bu.edu)
Date: 02/21/2025
"""

from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
    A Django ModelForm for creating a new Profile.

    Attributes:
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        city (CharField): The city of the user.
        email (EmailField): The email address of the user.
        profile_image_url (URLField): The profile image URL of the user.

    Meta:
        model (Profile): Specifies the Profile model.
        fields (list): Specifies the fields included in the form.
    """

    first_name = forms.CharField(label="First Name", required = True)
    last_name = forms.CharField(label="Last Name", required = True)
    city = forms.CharField(label="City", required = True)
    email = forms.EmailField(label="Email", required=True)
    profile_image_url = forms.CharField(label="Profile Image URL", required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']

class CreateStatusMessageForm(forms.ModelForm):
    """Form for posting a stust message"""
    class Meta:
        model = StatusMessage
        fields = ['message']    