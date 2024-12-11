# Generated by Django 5.1.1 on 2024-12-11 02:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_subfunctionvarvalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='task_Answer_bemodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('behavior_model_a_1', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='first', to='tasks.behaviormodel_a')),
                ('behavior_model_a_2', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='middle', to='tasks.behaviormodel_a')),
                ('behavior_model_b', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='last', to='tasks.behaviormodel_b')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_Answer_bemodel', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='task_Answer_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_code', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_Answer_code', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskVarValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='TaskVarValue', to='tasks.task')),
                ('var', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.behaviormodel_a')),
            ],
        ),
    ]