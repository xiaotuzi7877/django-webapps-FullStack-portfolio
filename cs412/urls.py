"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
#  allows you to connect URLs from different apps to the main urls.py

urlpatterns = [
    path('admin/', admin.site.urls),
    # For any request to the root URL (/), look for more URL patterns inside quotes/urls.py.
    path('quotes/', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('mini_fb/', include('mini_fb.urls')),
    # path('voter_analystics/', include('voter_analytics.urls')),
    path('accounts/', include('circuits.auth_urls')),
    path('circuits/', include('circuits.urls', namespace='circuits')),
]

# enable media file serving in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
