# Generated by Django 3.1.5 on 2021-02-16 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210215_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='category',
        ),
        migrations.AddField(
            model_name='listing',
            name='category',
            field=models.ManyToManyField(to='auctions.Category'),
        ),
    ]
