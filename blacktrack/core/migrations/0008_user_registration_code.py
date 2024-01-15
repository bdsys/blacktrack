# Generated by Django 3.2.6 on 2021-09-12 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210911_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_registration_code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_code', models.CharField(help_text='Enter the registration code given to you.', max_length=200)),
                ('usage_counter', models.IntegerField(default=0, null=True)),
            ],
        ),
    ]
