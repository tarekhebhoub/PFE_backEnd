# Generated by Django 4.1.7 on 2023-06-04 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_station_reservation_station_restauration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='reservation',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='station',
            name='restauration',
            field=models.IntegerField(default=5),
        ),
    ]
