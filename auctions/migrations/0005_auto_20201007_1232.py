# Generated by Django 3.1.2 on 2020-10-07 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20201006_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='price',
            field=models.IntegerField(),
        ),
    ]
