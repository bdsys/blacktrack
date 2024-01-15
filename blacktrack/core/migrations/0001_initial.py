# Generated by Django 3.2.6 on 2021-09-08 03:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='acquisition_location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the acquisition locations name (E.g. Albertsons, Costco, manufacturer direct, etc.', max_length=200)),
                ('acquisition_location_url', models.TextField(blank=True, help_text='Enter the acquisition locations URL', max_length=1000, null=True)),
                ('acquisition_location_country', models.CharField(blank=True, help_text='Enter the acquisition locations country', max_length=200, null=True)),
                ('acquisition_location_locality', models.CharField(blank=True, help_text='Enter the acquisition locations locality', max_length=200, null=True)),
                ('acquisition_location_city', models.CharField(blank=True, help_text='Enter the acquisition locations city', max_length=2000, null=True)),
                ('acquisition_location_address_line_1', models.TextField(blank=True, help_text='Enter the acquisition locations address "line 1"', max_length=1000, null=True)),
                ('acquisition_location_address_line_2', models.TextField(blank=True, help_text='Enter the acquisition locations address "line 2"', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='acquisition_source',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('acquisition_location_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.acquisition_location')),
            ],
        ),
        migrations.CreateModel(
            name='container_object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='container_object_instance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular item across the entire account.', primary_key=True, serialize=False)),
                ('container_object_instance_nickname', models.CharField(default='my-container', max_length=100)),
                ('location_in_site', models.CharField(blank=True, max_length=200)),
                ('serial_number', models.CharField(blank=True, max_length=400)),
                ('container_acquisition_date', models.DateField(blank=True, null=True)),
                ('container_warranty_bool', models.BooleanField(default=False)),
                ('container_warranty_expiration_date', models.DateField(blank=True, null=True)),
                ('container', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.container_object')),
            ],
            options={
                'ordering': ['site', 'container'],
            },
        ),
        migrations.CreateModel(
            name='container_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the container type (E.g. refrigerator, pantry, etc.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='item_object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='item_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the item type (E.g. new york steak, captain crunch, etc.', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='manufacturer_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the manufacturers name (E.g. Samsung, LG, home-made, etc.', max_length=200)),
                ('location_url', models.TextField(blank=True, help_text='Enter the manufacturers URL', max_length=1000, null=True)),
                ('location_country', models.CharField(blank=True, help_text='Enter the manufacturers country', max_length=200, null=True)),
                ('location_locality', models.CharField(blank=True, help_text='Enter the manufacturers locality', max_length=200, null=True)),
                ('location_city', models.CharField(blank=True, help_text='Enter the manufacturers city', max_length=2000, null=True)),
                ('location_address_line_1', models.TextField(blank=True, help_text='Enter the manufacturers address "line 1"', max_length=1000, null=True)),
                ('location_address_line_2', models.TextField(blank=True, help_text='Enter the manufacturers address "line 2"', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='site_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter the sites name (E.g. home, LG, guest house, etc.', max_length=200)),
                ('site_location_url', models.TextField(blank=True, help_text='Enter the sites URL', max_length=1000, null=True)),
                ('site_location_country', models.CharField(blank=True, help_text='Enter the sites country', max_length=200, null=True)),
                ('site_location_locality', models.CharField(blank=True, help_text='Enter the sites locality', max_length=200, null=True)),
                ('site_location_city', models.CharField(blank=True, help_text='Enter the sites city', max_length=2000, null=True)),
                ('site_location_address_line_1', models.TextField(blank=True, help_text='Enter the sites address "line 1"', max_length=1000, null=True)),
                ('site_location_address_line_2', models.TextField(blank=True, help_text='Enter the sites address "line 2"', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='model_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('container_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.container_type')),
                ('manufacturer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.manufacturer_type')),
            ],
        ),
        migrations.CreateModel(
            name='item_object_instance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular item across the entire account.', primary_key=True, serialize=False)),
                ('item_object_instance_nickname', models.CharField(default='my-item', max_length=100)),
                ('package_count', models.IntegerField(default=1, null=True)),
                ('number_in_package_count', models.IntegerField(default=1, null=True)),
                ('location_in_container', models.CharField(blank=True, max_length=200)),
                ('item_acquisition_date', models.DateField(blank=True, null=True)),
                ('item_deep_storage', models.BooleanField(default=False)),
                ('item_expiration_date', models.DateField(blank=True, null=True)),
                ('container_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.container_object_instance')),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.item_object')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.acquisition_source')),
            ],
            options={
                'ordering': ['container_instance', 'item'],
            },
        ),
        migrations.AddField(
            model_name='item_object',
            name='item_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.item_type'),
        ),
        migrations.AddField(
            model_name='item_object',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.manufacturer_type'),
        ),
        migrations.AddField(
            model_name='container_object_instance',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.site_type'),
        ),
        migrations.AddField(
            model_name='container_object_instance',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.acquisition_source'),
        ),
        migrations.AddField(
            model_name='container_object',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.model_type'),
        ),
        migrations.CreateModel(
            name='custom_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
