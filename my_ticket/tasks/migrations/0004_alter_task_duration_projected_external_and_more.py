# Generated by Django 5.2 on 2025-05-03 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_project_total_projected_time_external_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='duration_projected_external',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='duration_projected_internal',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='duration_registered',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
