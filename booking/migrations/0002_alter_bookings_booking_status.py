# Generated by Django 4.1.4 on 2022-12-18 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("booking", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bookings",
            name="booking_status",
            field=models.CharField(
                choices=[
                    ("BOOKED", "Booked"),
                    ("COMPLETED", "Completed"),
                    ("CANCELLED", "Cancelled"),
                ],
                default="BOOKED",
                max_length=50,
            ),
        ),
    ]
