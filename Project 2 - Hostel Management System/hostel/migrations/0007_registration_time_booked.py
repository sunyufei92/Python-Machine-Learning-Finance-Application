# Generated by Django 4.0.1 on 2022-01-24 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0006_registration_regno'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='time_booked',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
