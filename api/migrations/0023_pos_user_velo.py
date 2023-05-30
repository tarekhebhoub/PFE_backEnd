# Generated by Django 4.1.7 on 2023-05-29 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_user_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='pos_user',
            name='velo',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='pos_of_user_velo', to='api.velo'),
            preserve_default=False,
        ),
    ]
