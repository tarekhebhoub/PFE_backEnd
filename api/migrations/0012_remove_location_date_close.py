# Generated by Django 4.1.7 on 2023-05-03 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_location_reservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='date_close',
        ),
    ]
