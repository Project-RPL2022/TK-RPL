# Generated by Django 3.2.8 on 2022-12-03 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0002_alter_roomorder_guest_roompayment_checkout'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.FloatField(default=500),
        ),
    ]