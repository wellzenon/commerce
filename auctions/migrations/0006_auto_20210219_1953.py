# Generated by Django 3.1.5 on 2021-02-19 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210217_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
