# Generated by Django 2.2 on 2020-01-04 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0004_task_due_date'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='task',
            managers=[
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='is_complete',
            field=models.BooleanField(default=False),
        ),
    ]
