# Generated by Django 5.1.1 on 2024-12-11 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_task_answer_bemodel_task_answer_code_taskvarvalue'),
    ]

    operations = [
        migrations.AddField(
            model_name='subfunction',
            name='is_special',
            field=models.BooleanField(default=False),
        ),
    ]