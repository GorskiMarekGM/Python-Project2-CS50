# Generated by Django 3.1.2 on 2020-10-08 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_photo_article_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='article_image',
            field=models.ImageField(blank=True, upload_to='../media'),
        ),
    ]
