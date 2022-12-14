# Generated by Django 4.0.5 on 2022-11-20 05:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='followers',
        ),
        migrations.AddField(
            model_name='follow',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='follow',
            name='following',
        ),
        migrations.AddField(
            model_name='follow',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following', to=settings.AUTH_USER_MODEL),
        ),
        migrations.RemoveField(
            model_name='likes',
            name='liked_user',
        ),
        migrations.AddField(
            model_name='likes',
            name='liked_user',
            field=models.ManyToManyField(related_name='likes_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
