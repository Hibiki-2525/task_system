# Generated by Django 5.1.1 on 2024-12-12 06:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_pretestanswer_protestanswer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='protestanswer',
            name='submitted_at',
        ),
    ]
