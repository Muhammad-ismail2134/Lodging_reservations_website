# Generated by Django 4.2.2 on 2023-07-10 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0013_rename_a_price_booking_a_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='a_booked_from',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='a_booked_till',
            field=models.DateField(null=True),
        ),
    ]
