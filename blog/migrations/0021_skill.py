# Generated by Django 5.0 on 2024-01-23 05:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_contact_query_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo', models.ImageField(upload_to='logos')),
            ],
        ),
    ]
