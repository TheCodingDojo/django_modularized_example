# Generated by Django 2.2 on 2020-01-05 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0005_auto_20200103_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_at',
            field=models.DateTimeField(null=True),
        ),
    ]
