# Generated by Django 3.1.12 on 2021-12-26 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20211226_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='classification',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]