# Generated by Django 5.0 on 2024-01-17 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_team'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='profile',
        ),
    ]