# Generated by Django 3.2.6 on 2021-09-11 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210910_0230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='acquisition_location',
            name='acquisition_url',
            field=models.URLField(blank=True, help_text='Enter the acquisition locations URL', max_length=2000, null=True),
        ),
        migrations.AlterField(
            model_name='manufacturer_type',
            name='manufacturer_url',
            field=models.URLField(blank=True, help_text='Enter the manufacturers URL', max_length=2000, null=True),
        ),
    ]
