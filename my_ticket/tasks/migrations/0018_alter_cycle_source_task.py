# Generated by Django 5.2 on 2025-05-11 17:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0017_alter_task_prerequisites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycle',
            name='source_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tasks.task'),
        ),
    ]
