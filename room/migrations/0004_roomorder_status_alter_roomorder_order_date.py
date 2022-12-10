# Generated by Django 4.1.3 on 2022-12-09 17:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_room_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomorder',
            name='status',
            field=models.CharField(choices=[('OCCUPYING', 'OCCUPYING'), ('FINISHED', 'FINISHED')], default='OCCUPYING', max_length=30),
        ),
        migrations.AlterField(
            model_name='roomorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 0, 0, 6, 129439)),
        ),
    ]