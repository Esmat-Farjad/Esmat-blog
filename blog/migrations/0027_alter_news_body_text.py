# Generated by Django 5.0 on 2024-02-25 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0026_remove_news_post_url_remove_news_project_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='body_text',
            field=models.TextField(max_length=300),
        ),
    ]
