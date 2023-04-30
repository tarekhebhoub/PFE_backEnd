# Generated by Django 4.1.7 on 2023-04-30 07:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_location_reservation_alter_reservation_velo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='reservation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservation_alocate', to='api.reservation'),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='velo',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='velo_located', to='api.velo'),
        ),
    ]
