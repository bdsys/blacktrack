# Generated by Django 3.2.6 on 2021-09-08 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210908_0417'),
    ]

    operations = [
        migrations.AddField(
            model_name='acquisition_location',
            name='acquisition_url',
            field=models.URLField(help_text='Enter the acquisition locations URL', max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='manufacturer_type',
            name='manufacturer_url',
            field=models.URLField(help_text='Enter the manufacturers URL', max_length=2000, null=True),
        ),
    ]
