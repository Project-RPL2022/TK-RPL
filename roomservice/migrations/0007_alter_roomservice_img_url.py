# Generated by Django 4.1.3 on 2022-12-08 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roomservice', '0006_roomservice_img_url_roomservice_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomservice',
            name='img_url',
            field=models.CharField(default='https://upload.wikimedia.org/wikipedia/commons/1/14/No_Image_Available.jpg', max_length=255),
        ),
    ]
