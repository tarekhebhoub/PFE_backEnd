# Generated by Django 4.1.7 on 2023-07-24 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_employee_echelle_employee_id_struc'),
    ]

    operations = [
        migrations.CreateModel(
            name='OffreEMP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TitreOffre', models.CharField(max_length=50)),
                ('NombrePoste', models.IntegerField()),
                ('Description', models.FileField(upload_to='file/')),
            ],
        ),
    ]