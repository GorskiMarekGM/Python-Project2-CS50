# Generated by Django 3.1.2 on 2020-10-19 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0030_auto_20201019_1033'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction',
            name='creator',
        ),
    ]
