# Generated by Django 3.1.2 on 2020-12-22 19:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_account'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Account',
            new_name='Birthdate',
        ),
        migrations.RenameField(
            model_name='birthdate',
            old_name='birthday',
            new_name='birthdate',
        ),
    ]
