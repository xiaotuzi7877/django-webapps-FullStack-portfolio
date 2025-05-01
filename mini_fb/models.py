# File: models.py
# Author: Li Ziyang (miclilzy@bu.edu), 02/21/2025
# Description: Defines the Profile model, which represents user profile information 
# in the Django application, including name, city, email, and profile image URL.
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



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
    # link profile to Django User
    user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)



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
    
    def get_friends(self):
        """
        Returns a list of Profile objects that are friends with this Profile.
        """
        # Retrieve all Friend instances where this profile is profile1 or profile2
        friends = Friend.objects.filter(profile1=self) | Friend.objects.filter(profile2=self)

        # Extract the Profile objects (excluding self)
        friend_profiles = [
            friend.profile2 if friend.profile1 == self else friend.profile1
            for friend in friends
        ]

        return friend_profiles
    
    def add_friend(self, other):
        """
        Adds a friend relation if it does not already exist and avoids self-friending.
        """
        if self == other:
            return  # Prevent self-friending

        # Check if the friendship already exists
        friendship_exists = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        if not friendship_exists:
            Friend.objects.create(profile1=self, profile2=other)

    def get_friend_suggestions(self):
        """
        Returns a list of potential friends that the user is not yet friends with.
        """
        # Get IDs of current friends
        friend_ids = [friend.pk for friend in self.get_friends()]

         # Return all profiles excluding self and existing friends
        return Profile.objects.exclude(pk=self.pk).exclude(pk__in=friend_ids)
    
    def get_news_feed(self):
        """
        Returns a queryset of status messages from the profile and its friends, sorted by timestamp.
        """
        # Get the list of friends
        friends = self.get_friends()

        # Get status messages for this profile and their friends
        status_messages = StatusMessage.objects.filter(
            models.Q(profile=self) | models.Q(profile__in=friends)
        ).order_by('-timestamp')  # Most recent first

        return status_messages
    
    
    
class StatusMessage(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set the timestamp when created
    message = models.TextField()  # The text content of the status message
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)  # Relationship to Profile

    def __str__(self):
        return f"Status by {self.profile.first_name} at {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
class Image(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank = True, null = True)

class StatusImage(models.Model):
    status_message = models.ForeignKey(StatusMessage, on_delete = models.CASCADE)
    image = models.ForeignKey(Image, on_delete = models.CASCADE)

class Friend(models.Model):
    """
    represents a friendship connection between 2 profiles
    """
    profile1 = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = "friends_profile1")
    profile2 = models.ForeignKey(Profile, on_delete = models.CASCADE, related_name = "friends_profile2")
    timestamp = models.DateTimeField(auto_now_add = True) # stores the time of making connections

    def __str__(self):
        """
        String representation of friendship
        """
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"
    
    class Meta:
        """
        Ensure that the combination of profile1 and profile2 is unique
        Prevents duplicate friendships like (A, B) and (A, B) from being created"
        """
        unique_together = ('profile1', 'profile2')