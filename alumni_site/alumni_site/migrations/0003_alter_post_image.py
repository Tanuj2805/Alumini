# Generated by Django 4.1.13 on 2025-04-08 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alumni_site', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/posts/'),
        ),
    ]
