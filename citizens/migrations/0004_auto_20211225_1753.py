# Generated by Django 3.1.12 on 2021-12-25 10:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('citizens', '0003_auto_20211225_1537'),
    ]

    operations = [
        migrations.RenameField(
            model_name='citizen',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RemoveField(
            model_name='citizen',
            name='last_name',
        ),
    ]
