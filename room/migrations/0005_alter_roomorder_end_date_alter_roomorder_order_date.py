# Generated by Django 4.1.3 on 2022-12-09 17:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0004_roomorder_status_alter_roomorder_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomorder',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='roomorder',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 10, 0, 2, 19, 998616)),
        ),
    ]