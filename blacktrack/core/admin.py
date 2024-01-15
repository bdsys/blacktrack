from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import item_type, item_object, manufacturer_type, container_type, model_type, \
container_object, item_object_instance, container_object_instance, site_type, acquisition_source, \
acquisition_location, custom_user, address_type, user_registration_code, group_roster

# Register forms
from .forms import UserRegistrationForm, UserRegistrationCodeForm

# Register base models
admin.site.register(container_type)
admin.site.register(item_type)
admin.site.register(manufacturer_type)
admin.site.register(site_type)
admin.site.register(acquisition_location)
admin.site.register(address_type)
admin.site.register(user_registration_code)
admin.site.register(custom_user)

# t2 - item_object, model_type, container_object, acquisition_source
# Register tier 2 models
# Register the Admin classes for item_object using the decorator

@admin.register(group_roster)
class groupRosterAdmin(admin.ModelAdmin):
    list_display = ('custom_user_id','group_id','group_status')

@admin.register(item_object)
class ItemObjectAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'item_type', 'manufacturer')
    
@admin.register(model_type)
class ModelTypeAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'container_type', 'manufacturer')
    
@admin.register(container_object)
class ContainerTypeAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'model')
    
@admin.register(acquisition_source)
class AcquisitionSourceAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'acquisition_location_1')


# t3 - container_object_instance
# Register tier 3 models

@admin.register(container_object_instance)
class ContainerObjectInstanceAdmin(admin.ModelAdmin):
    
    list_display = ('container', 'site', 'serial_number', 'id', 'container_object_instance_nickname', 'group_owner')
    
# t4 - item_object_instance
# Register tier 4 models

@admin.register(item_object_instance)
class ItemObjectInstanceAdmin(admin.ModelAdmin):
    
    list_display = ('item_object_instance_nickname', 'item', 'item_expiration_date', 'id', 'group_owner')
    # list_filter = ('item_expiration_date')

    fieldsets = (
        (None, {
            'fields': ('item','item_object_instance_nickname', 'container_instance', 'source', 'group_owner')
        }),
        ('Specifics', {
            'fields': ('package_count', 'number_in_package_count','location_in_container', 'item_acquisition_date', 'item_deep_storage', 'item_expiration_date')
        }),
    )

