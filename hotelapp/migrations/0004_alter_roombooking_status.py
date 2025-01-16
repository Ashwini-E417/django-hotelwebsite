# Generated by Django 5.1.2 on 2024-11-02 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0003_roombooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roombooking',
            name='status',
            field=models.IntegerField(choices=[(1, 'Success'), (2, 'Booked'), (3, 'Canceled')]),
        ),
    ]
