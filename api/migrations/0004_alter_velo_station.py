# Generated by Django 4.1.7 on 2023-04-30 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_rename_resevation_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='velo',
            name='station',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='velos', to='api.station'),
        ),
    ]
