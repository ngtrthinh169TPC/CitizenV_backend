# Generated by Django 3.1.12 on 2021-12-26 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20211225_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='classification',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]