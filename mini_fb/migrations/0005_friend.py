# Generated by Django 5.1.6 on 2025-03-21 21:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mini_fb', '0004_image_statusimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('profile1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends_profile1', to='mini_fb.profile')),
                ('profile2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friends_profile2', to='mini_fb.profile')),
            ],
            options={
                'unique_together': {('profile1', 'profile2')},
            },
        ),
    ]
