# Generated by Django 4.1.7 on 2023-05-29 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0020_alter_user_usage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="usage",
            field=models.IntegerField(default=0),
        ),
    ]
