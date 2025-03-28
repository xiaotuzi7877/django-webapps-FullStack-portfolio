# mini_fb/management/commands/load_profiles.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from mini_fb.models import Profile

class Command(BaseCommand):
    help = 'Load predefined users and profiles into the database.'

    def handle(self, *args, **kwargs):
        username = "non_admin"
        password = "testpassword123"
        email = "nonadmin@example.com"

        # Check if user exists
        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        if created:
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✅ User "{username}" created.'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ User "{username}" already exists.'))

        # Check if profile exists
        if not hasattr(user, 'profile'):
            profile = Profile.objects.create(
                user=user,
                first_name="Guanyu",
                last_name="Zhou",
                city="Shanghai",
                email=email,
                profile_image_url="mini_fb/images/Zhou.jpg"
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Profile for "{username}" created.'))
        else:
            self.stdout.write(self.style.WARNING(f'⚠️ Profile for "{username}" already exists.'))
