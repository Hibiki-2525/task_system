# Generated by Django 5.1.1 on 2024-12-14 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0012_alter_answer_bemodel_behavior_model_a_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer_bemodel',
            name='behavior_model_c',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inout', to='tasks.behaviormodel_c'),
        ),
        migrations.AddField(
            model_name='task_answer_bemodel',
            name='behavior_model_c',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_inout', to='tasks.behaviormodel_c'),
        ),
    ]