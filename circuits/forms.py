# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Defines Django forms used in the 'circuits' application,
# including forms for adding comments and user signup.

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, LapTimeEntry, Profile


class CommentForm(forms.ModelForm):
    """
    A form based on the Comment model, used for creating and updating comments.
    Specifies the fields, widgets, labels, and help texts for the form.
    """
    
    class Meta:
        model = Comment
        # Fields from the Comment model to include in the form
        fields = ['text', 'rating'] 
        
        # Customize the HTML widgets used for form fields
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', # Apply Bootstrap class
                'placeholder': 'Enter your comment here...', # Placeholder text
                'rows': 3, # Set default textarea height
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select', # Apply Bootstrap class
            }),
        }
        # Customize the labels displayed for form fields
        labels = {
            'text': 'Comment',
            'rating': 'Rating',
        }
        # Provide additional help text displayed below form fields
        help_texts = {
            'rating': 'Choose a rating from 1 (worst) to 5 (best).',
        }

class SignUpForm(UserCreationForm):
    """
    A form for new user registration, inheriting from Django's UserCreationForm.
    Adds a required email field and specifies the fields to be included.
    """
    # Add an email field, making it required for signup
    email = forms.EmailField(
        required=True, 
        help_text='Required. Please enter a valid email address.'
        ) 

    class Meta:
        # Inherit model from the parent UserCreationForm (which is User)
        model = User 
        # Specify the fields to include in the registration form
        fields = ['username', 'email', 'password1', 'password2']

class LapTimeForm(forms.ModelForm):
    class Meta:
        model = LapTimeEntry
        fields = ['car', 'lap_time'] 
        widgets = {
            'car': forms.Select(attrs={'class': 'form-select'}),
            'lap_time': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., 1:23.456'
            }),
        }

class ProfileForm(forms.ModelForm):
    """
    Form for users to update their profile information, specifically the avatar.
    """
    class Meta:
        model = Profile
        fields = ['avatar'] 
        widgets = {
            
            'avatar': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'avatar': 'Upload a new avatar', 
        }
        help_texts = {
            'avatar': 'Select an image file for your profile picture.',
        }