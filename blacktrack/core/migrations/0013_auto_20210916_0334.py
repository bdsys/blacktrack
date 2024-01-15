# Generated by Django 3.2.6 on 2021-09-16 03:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '0012_remove_group_roster_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='container_object_instance',
            name='group_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
        migrations.AddField(
            model_name='item_object_instance',
            name='group_owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]
