# Generated by Django 4.1.7 on 2023-05-28 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0015_alter_pos_user_latitude_alter_pos_user_longitude_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="sold",
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name="user",
            name="usage",
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name="velo",
            name="station",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="velos",
                to="api.station",
            ),
        ),
    ]
