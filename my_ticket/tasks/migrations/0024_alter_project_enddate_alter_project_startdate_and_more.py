# Generated by Django 5.2 on 2025-06-22 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0023_alter_meetingcontextcontact_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='enddate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='startdate',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_projected_time_external',
            field=models.TimeField(default='00:00.000', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='total_projected_time_internal',
            field=models.TimeField(default='00:00.000', null=True),
        ),
    ]
