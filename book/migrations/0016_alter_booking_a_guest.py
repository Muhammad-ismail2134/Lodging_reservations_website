# Generated by Django 4.2.2 on 2023-07-11 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0015_alter_card_a_holder_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='a_guest',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
