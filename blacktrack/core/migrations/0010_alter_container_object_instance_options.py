# Generated by Django 3.2.6 on 2021-09-15 06:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_alter_item_object_instance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='container_object_instance',
            options={'ordering': ['site', 'container'], 'permissions': (('can_create_container_object_instance', 'Create new container object instances'), ('can_update_container_object_instance', 'Update existing container object instances'), ('can_delete_container_object_instance', 'Delete existing container object instances'))},
        ),
    ]
