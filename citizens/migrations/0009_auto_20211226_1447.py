# Generated by Django 3.1.12 on 2021-12-26 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0008_auto_20211225_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'male'), ('Female', 'female'), ('unknown', 'unknown')], max_length=8),
        ),
    ]
