# Generated by Django 3.1.12 on 2021-12-26 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0009_auto_20211226_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='gender',
            field=models.CharField(choices=[('Male', 'male'), ('Female', 'female'), ('unknown', 'unknown')], max_length=8),
        ),
    ]
