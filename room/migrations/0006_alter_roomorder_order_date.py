# Generated by Django 4.1.3 on 2022-12-09 17:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0005_alter_roomorder_end_date_alter_roomorder_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 0, 54, 12, 983197)),
        ),
    ]
