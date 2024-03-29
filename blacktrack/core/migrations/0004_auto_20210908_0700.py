# Generated by Django 3.2.6 on 2021-09-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210908_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address_type',
            name='location_address_line_1',
            field=models.TextField(help_text='Enter address "line 1"', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='address_type',
            name='location_address_line_2',
            field=models.TextField(help_text='Enter address "line 2"', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='address_type',
            name='location_city',
            field=models.CharField(help_text='Enter the city', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='address_type',
            name='location_country',
            field=models.CharField(help_text='Enter the country', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address_type',
            name='location_locality',
            field=models.CharField(help_text='Enter the locality', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='address_type',
            name='location_zipcode',
            field=models.CharField(help_text='Enter the citys ZIP code', max_length=20, null=True),
        ),
    ]
