# circuits/admin.py

# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Configures the Django admin interface for the 'circuits'
# application models. Defines how models are displayed and managed
# within the admin site.

from django.contrib import admin
# --- NEW IMPORTS ---
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html # Optional: for displaying image preview
# --- END NEW IMPORTS ---

# Import all your models
from .models import (
    Circuit,
    Comment,
    Question,
    Choice,
    QuizAttempt,
    Answer,
    Profile,      # <-- Added Profile
    LapTimeEntry  # <-- Added LapTimeEntry
)

# ---------------------------------------------------
#   Inline Configuration for Profile within User Admin
# ---------------------------------------------------
class ProfileInline(admin.StackedInline): # Use StackedInline for better layout with ImageField
    """Inline admin descriptor for Profile model"""
    model = Profile
    can_delete = False # Don't allow deleting Profile from User admin
    verbose_name_plural = 'User Profile'
    fk_name = 'user'
    fields = ('avatar', 'avatar_preview',) # Add preview if desired
    readonly_fields = ('avatar_preview',) # Make preview read-only

    # Optional: Add a preview of the current avatar
    @admin.display(description='Current Avatar Preview')
    def avatar_preview(self, obj):
        if obj.avatar:
            # Render a small image tag; adjust width/height as needed
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />', obj.avatar.url)
        return "(No avatar)"

# ---------------------------------------------------
#   Custom User Admin with Profile Inline
# ---------------------------------------------------
class UserAdmin(BaseUserAdmin):
    """Define a new User admin with Profile inline"""
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_profile_avatar_status')
    list_select_related = ('circuits_profile',) # Optimize query

    # Method to show avatar status in the User list view
    @admin.display(description='Avatar Status')
    def get_profile_avatar_status(self, instance):
        try:
            # Use the correct related_name 'circuits_profile'
            if instance.circuits_profile and instance.circuits_profile.avatar:
                return "Uploaded"
            return "Missing"
        except Profile.DoesNotExist:
            return "No Profile Record" # Handle case where Profile might not exist yet

# Unregister the original User admin
admin.site.unregister(User)
# Register the User model using the custom UserAdmin
admin.site.register(User, UserAdmin)

# ---------------------------------------------------
#   Existing Admin Registrations (Keep these!)
# ---------------------------------------------------
@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    """Admin interface customization for the Circuit model."""
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface customization for the Comment model."""
    list_display = ('user', 'circuit', 'created_at', 'rating') # Added rating
    list_filter = ('circuit', 'created_at', 'rating') # Added rating
    search_fields = ('user__username', 'text', 'circuit__name') # Added circuit name

class ChoiceInline(admin.TabularInline):
    """Inline configuration for Choices"""
    model = Choice
    extra = 3

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface customization for the Question model."""
    list_display = ('text',)
    inlines = (ChoiceInline,)

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface customization for the QuizAttempt model."""
    list_display = ('user', 'start_time', 'end_time', 'score')
    list_filter = ('user',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin interface customization for the Answer model."""
    list_display = ('attempt', 'question', 'selected_choice', 'is_correct')
    list_filter = ('is_correct',)

# ---------------------------------------------------
#   NEW: Register LapTimeEntry
# ---------------------------------------------------
@admin.register(LapTimeEntry)
class LapTimeEntryAdmin(admin.ModelAdmin):
    """Admin interface customization for the LapTimeEntry model."""
    list_display = ('user', 'circuit', 'lap_time', 'car', 'created_at')
    list_filter = ('circuit', 'car', 'user')
    search_fields = ('user__username', 'circuit__name', 'lap_time')
    date_hierarchy = 'created_at' # Allows quick date navigation

# ---------------------------------------------------
#   Optional: Register Profile separately (if needed, but usually Inline is sufficient)
# ---------------------------------------------------
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ('user', 'avatar')
#     search_fields = ('user__username',)