# Generated by Django 5.1.2 on 2024-11-22 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0004_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comments',
            name='post',
        ),
    ]
