# Generated by Django 4.1.3 on 2022-12-08 19:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0010_alter_feedback_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 12, 9, 2, 0, 43, 401881)),
        ),
    ]