# Generated by Django 3.1.12 on 2021-12-23 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citizen',
            name='first_name',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]