# Generated by Django 3.2.6 on 2021-09-16 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20210916_0334'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group_roster',
            old_name='custom_user_id',
            new_name='custom_user',
        ),
        migrations.RenameField(
            model_name='group_roster',
            old_name='group_id',
            new_name='group',
        ),
        migrations.AddField(
            model_name='group_roster',
            name='group_status',
            field=models.CharField(blank=True, choices=[('o', 'Owner'), ('m', 'member'), ('r', 'readonly'), ('p', 'pending')], default='p', help_text='Group membership status', max_length=1),
        ),
    ]
