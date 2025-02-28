# File: models.py
# Author: Li Ziyang (miclilzy@bu.edu), 02/21/2025
# Description: Defines the Profile model, which represents user profile information 
# in the Django application, including name, city, email, and profile image URL.
from django.db import models
from django.urls import reverse



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
    
    def get_status_messages(self):
        """ return all status messages for this profile, ordered by timestamp (newst first)"""
        return self.statusmessage_set.all().order_by('-timestamp') 
    
    def get_absolute_url(self):
        """
        Returns the absolute URL for a profile instance, redirecting to the profile page after creation.
        """
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_message(self):
        """
        returns all status messages for this profile, ordered by timestamp.
        """
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        """
        returns the url to view this profile
        """
        return reverse("show_profile", kwargs={"pk": self.pk})
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when created
    message = models.TextField()  # The text content of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relationship to Profile

    def __str__(self):
        return f"Status by {self.profile.first_name} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

