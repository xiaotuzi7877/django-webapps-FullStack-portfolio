# Name: Li Ziyang
# BU Email: miclilzy@bu.edu
# File Description: Defines authentication-related URL patterns (login, logout) 
# using Django's built-in authentication views. This file is typically 
# included in the main project's urls.py under the 'accounts/' path.

from django.urls import path
from django.contrib.auth import views as auth_views

# This file usually doesn't need an app_name defined,
# so that {% url 'login' %} can be resolved globally without a namespace.

# List of authentication-related URL patterns
urlpatterns = [
    # Login URL
    path(
        'login/',  # Path relative to the include point (e.g., /accounts/), so full URL might be /accounts/login/
        auth_views.LoginView.as_view(
            # Specify the custom template for the login page
            template_name='circuits/login.html' 
        ),
        name='login' # URL name, used for {% url 'login' %} in templates/views
    ),

    # Logout URL
    path(
        'logout/', # Path relative to the include point, e.g., /accounts/logout/
        auth_views.LogoutView.as_view(
            # Specify the custom template shown after successful logout
            template_name='circuits/logged_out.html' 
            # Alternatively, to redirect after logout instead of showing a page:
            # next_page = 'circuits:circuit_list' # Example: Redirect to the circuit list page
        ),
        name='logout' # URL name, used for {% url 'logout' %}
    ),

]