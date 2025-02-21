# File: models.py
# Author: Li Ziyang (miclilzy@bu.edu), 02/21/2025
# Description: Defines the Profile model, which represents user profile information 
# in the Django application, including name, city, email, and profile image URL.
from django.db import models

# Create your models here.
from django.db import models

class Profile(models.Model):
    # User's first name (maximum length: 50 characters)
    first_name = models.CharField(max_length= 50)
    # User's last name (maximum length: 50 characters)
    last_name = models.CharField(max_length=50)
    # City where the user resides (maximum length: 50 characters)
    city = models.CharField(max_length=50)
    # Unique email address for the user
    email = models.EmailField(unique=True)
    # URL string for the user's profile image (maximum length: 50 characters)
    profile_image_url = models.CharField(max_length=50)

    # returns a readable representation of the profile).
    def __str__(self):
        return f"{self.first_name}{self.last_name}"
