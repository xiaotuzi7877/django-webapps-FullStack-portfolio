# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Configures the Django admin interface for the 'circuits' 
# application models. Defines how models are displayed and managed 
# within the admin site.

from django.contrib import admin
from .models import Circuit, Comment, Question, Choice, QuizAttempt, Answer

@admin.register(Circuit)
class CircuitAdmin(admin.ModelAdmin):
    """Admin interface customization for the Circuit model."""
    # Fields to display in the admin list view for Circuits
    list_display = ('name', 'location') 
    # Fields that can be searched via the admin search bar
    search_fields = ('name', 'location') 

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin interface customization for the Comment model."""
    # Fields to display in the admin list view for Comments
    list_display = ('user', 'circuit', 'created_at') 
    # Fields that can be used for filtering in the admin sidebar
    list_filter = ('circuit', 'created_at') 
    # Fields searchable via the admin search bar (includes related user's username)
    search_fields = ('user__username', 'text') 

class ChoiceInline(admin.TabularInline):
    """
    Inline configuration for Choices to be displayed within the Question admin page.
    Allows adding/editing Choices directly when viewing a Question.
    """
    # The model to display inline
    model = Choice 
    # Number of empty extra forms to display for adding new Choices
    extra = 3 

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin interface customization for the Question model."""
    # Fields to display in the admin list view for Questions
    list_display = ('text',) 
    # Include the ChoiceInline configuration to manage Choices within the Question page
    inlines = (ChoiceInline,) 

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """Admin interface customization for the QuizAttempt model."""
    # Fields to display in the admin list view for QuizAttempts
    list_display = ('user', 'start_time', 'end_time', 'score') 
    # Fields that can be used for filtering in the admin sidebar
    list_filter = ('user',) 

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Admin interface customization for the Answer model."""
    # Fields to display in the admin list view for Answers
    list_display = ('attempt', 'question', 'selected_choice', 'is_correct') 
    # Fields that can be used for filtering in the admin sidebar
    list_filter = ('is_correct',)