# Generated by Django 4.2.3 on 2023-09-23 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_fichierbourse_allright'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fichierbourse',
            name='response_Dep',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]