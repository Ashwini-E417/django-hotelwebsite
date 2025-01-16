# Generated by Django 5.1.2 on 2024-11-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotelapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rooms',
            name='bedtypecat',
            field=models.IntegerField(choices=[(1, 'Single'), (2, 'Double'), (3, 'Multiple')], verbose_name='Bed Type'),
        ),
    ]
