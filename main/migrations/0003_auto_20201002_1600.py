# Generated by Django 3.0.8 on 2020-10-02 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_task_state'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='state',
            new_name='isDone',
        ),
    ]
