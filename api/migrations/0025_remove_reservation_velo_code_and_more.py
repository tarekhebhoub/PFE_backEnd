# Generated by Django 4.1.7 on 2023-05-30 22:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_reservation_velo_code_reservation_velo_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='velo_code',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='velo_name',
        ),
    ]
