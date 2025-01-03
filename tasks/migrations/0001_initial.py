# Generated by Django 5.1.1 on 2024-12-02 16:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubFunction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='tasks.subfunction')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subfunctions', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='Answer_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct_code', models.TextField()),
                ('sub_function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Answer_code', to='tasks.subfunction')),
            ],
        ),
        migrations.CreateModel(
            name='Answer_bemodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bemodel', models.CharField(max_length=255)),
                ('sub_function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Answer_bemodel', to='tasks.subfunction')),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(max_length=200)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Card', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='BehaviorModel_B',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='b_choices', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='BehaviorModel_A',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='a_choices', to='tasks.task')),
            ],
        ),
    ]
