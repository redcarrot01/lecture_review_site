# Generated by Django 3.0.5 on 2020-08-19 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='date_of_birth',
        ),
    ]
