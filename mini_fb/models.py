from django.db import models

# Create your models here.
from django.db import models

class Profile(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    profile_image_url = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"
