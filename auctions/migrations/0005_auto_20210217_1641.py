# Generated by Django 3.1.5 on 2021-02-17 16:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210217_0304'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='categories',
            new_name='category',
        ),
    ]
