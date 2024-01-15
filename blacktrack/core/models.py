from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid # unique objects
from django.contrib.auth.models import AbstractUser, Group # Django's base user model for further customization via data model
from .managers import CustomUserManager # Import class from managers.py substituting email for username in base user model in the datastore queries
from django.utils import timezone

# Datetime math
from datetime import date

# Auth models

# Custom user
# Modification to Django base user
class custom_user(AbstractUser):
    username = None
    email = models.EmailField(('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    # All objects for this class come from the .managers.py import class "CustomUserManager()"
    objects = CustomUserManager()

    permissions = (
        ("can_create_custom_user", "Create new custom_user objects"),
        ("can_update_custom_user", "Update existing custom_user objects"),
        ("can_delete_custom_user", "Delete existing custom_user objects"),
    )

    def __str__(self):
        return self.email
        
class user_registration_code(models.Model):
    """Model representing a user registrations code."""
    registration_code = models.CharField(max_length=200, help_text='Enter the registration code given to you.')
    usage_counter = models.IntegerField(default = 0, null=True)

    permissions = (
        ("can_create_user_registration_code", "Create new user_registration_code objects"),
        ("can_update_user_registration_code", "Update existing user_registration_code objects"),
        ("can_delete_user_registration_code", "Delete existing user_registration_code objects"),
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.registration_code
        

# Group to owner relationship

class group_roster(models.Model):
    """Model representing the relationship between a custom_user and an auth_group"""
    
    custom_user = models.ForeignKey(custom_user, blank=False, on_delete=models.RESTRICT, null=True)
    group = models.ForeignKey(Group, blank=False, on_delete=models.RESTRICT, null=True)

    status = (
        ('o', 'Owner'),
        ('m', 'member'),
        ('r', 'readonly'),
        ('p', 'pending'),
    )
    
    group_status = models.CharField(
        max_length=1,
        choices=status,
        blank=True,
        default='p',
        help_text='Group membership status',
    )

    def __int__(self):
        """String for representing the Model object."""
        return self.group

# Base models (tier 1) -- no upstream relationships

# container_type model
class container_type(models.Model):
    """Model representing a container type."""
    name = models.CharField(max_length=200, help_text='Enter the container type (E.g. refrigerator, pantry, etc.)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

# item_type model
class item_type(models.Model):
    """Model representing an item type."""
    name = models.CharField(max_length=200, help_text='Enter the item type (E.g. new york steak, captain crunch, etc.)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
# address_type model
class address_type(models.Model):
    """Model representing an address type."""
    name = models.CharField(max_length=200, help_text='Enter the address''s name')
    
    location_country = models.CharField(max_length=200, blank=True, null=True, help_text='Enter the country')
    location_locality = models.CharField(max_length=200, blank=True, null=True, help_text='Enter the locality')
    location_city = models.CharField(max_length=2000, blank=True, null=True, help_text='Enter the city')
    location_zipcode = models.CharField(max_length=20, blank=True, null=True, help_text='Enter the city''s ZIP code')
    location_address_line_1 = models.TextField(max_length=1000, blank=True, null=True, help_text='Enter address "line 1"')
    location_address_line_2 = models.TextField(max_length=1000, blank=True, null=True, help_text='Enter address "line 2"')
    
        # Custom properties
    
    # Property which returns a bool indicating if any location information is present
    @property
    def contains_location_data(self):
        
        ContainsLocationDataBool = False
        
        if self.location_country is not None or \
        self.location_locality is not None or \
        self.location_city is not None or \
        self.location_zipcode is not None or \
        self.location_address_line_1 is not None or \
        self.location_address_line_2 is not None:
            
            ContainsLocationDataBool = True
        
        return ContainsLocationDataBool
    
    class Meta:
        permissions = (
            ("can_create_address", "Create new address objects"),
            ("can_update_address", "Update existing address objects"),
            ("can_delete_address", "Delete existing address objects"),
        )
        
    def get_absolute_url(self):
        """Returns the url to access a particular address object."""
        return reverse('address-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name


# manufacturer_type model
class manufacturer_type(models.Model):
    """Model representing a manufacturer type."""
    name = models.CharField(max_length=200, help_text='Enter the manufacturer''s name (E.g. Samsung, LG, home-made, etc.)')
    manufacturer_address = models.ForeignKey(address_type, blank=True, on_delete=models.SET_NULL, null=True)
    manufacturer_url = models.URLField(max_length=2000, help_text='Enter the manufacturer''s URL', blank=True, null=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

# site_type model
class site_type(models.Model):
    """Model representing an site type."""
    name = models.CharField(max_length=200, help_text='Enter the site''s name (E.g. home, LG, guest house, etc.)')
    site_address = models.ForeignKey(address_type, blank=True, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        permissions = (
            ("can_create_site", "Create new Site objects"),
            ("can_update_site", "Update existing Site objects"),
            ("can_delete_site", "Delete existing Site objects"),
        )
        
    def get_absolute_url(self):
        """Returns the url to access a particular site object."""
        return reverse('site-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
# acquisition_location model
class acquisition_location(models.Model):
    """Model representing an site type."""
    name = models.CharField(max_length=200, help_text='Enter the acquisition location''s name (E.g. Albertsons, Costco, manufacturer direct, etc.)')
    acquisition_address = models.ForeignKey(address_type, blank=True, on_delete=models.SET_NULL, null=True)
    acquisition_url = models.URLField(max_length=2000, help_text='Enter the acquisition location''s URL', blank=True, null=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name
    
        
# Tier 2 models -- only tier 1 upstream relationships

# item_object model
class item_object(models.Model):
    """Model representing an Item (but not a specific copy of an item)."""
    name = models.CharField(max_length=200)

    # Foreign Key used because item_object can only have one item_type, but item_type can have multiple item_objects
    item_type = models.ForeignKey(item_type, on_delete=models.SET_NULL, null=True)

    manufacturer = models.ForeignKey(manufacturer_type, blank=True, on_delete=models.SET_NULL, null=True)
    
    # model specific functions

    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
# model_type model
class model_type(models.Model):
    """Model representing a model of a manufacturer_type's products."""
    name = models.CharField(max_length=200)
    container_type = models.ForeignKey(container_type, blank=True, on_delete=models.SET_NULL, null=True)
    manufacturer = models.ForeignKey(manufacturer_type,on_delete=models.SET_NULL, null=True)
    
    # model specific functions

    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
# container_object model
class container_object(models.Model):
    """Model representing a container."""
    name = models.CharField(max_length=200)
    model = models.ForeignKey(model_type, blank=True, on_delete=models.SET_NULL, null=True)
    
    # model specific functions

    def __str__(self):
        """String for representing the Model object."""
        return self.name
        
# item_source model
class acquisition_source(models.Model):
    """Model representing the source of an item_object_instance."""
    name = models.CharField(max_length=200)
    acquisition_location_1 = models.ForeignKey(acquisition_location, blank=True, on_delete=models.SET_NULL, null=True)
    
    # model specific functions

    def __str__(self):
        """String for representing the Model object."""
        return self.name


# Tier 3 models -- at least 1 tier 2 upstream relationship

# container_object_instance model
class container_object_instance(models.Model):
    """Model representing a specific copy of an container_object."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular item across the entire account.')
    container_object_instance_nickname = models.CharField(max_length=100, blank=False, default="my-container")
    # container = models.ForeignKey(container_object, on_delete=models.RESTRICT, null=True)
    # source = models.ForeignKey(acquisition_source, blank=True, on_delete=models.RESTRICT, null=True)
    # site = models.ForeignKey(site_type, on_delete=models.RESTRICT, null=True)
    container = models.ForeignKey(container_object, on_delete=models.SET_NULL, null=True)
    source = models.ForeignKey(acquisition_source, blank=True, on_delete=models.SET_NULL, null=True)
    site = models.ForeignKey(site_type, on_delete=models.SET_NULL, null=True)
    location_in_site = models.CharField(max_length=200, blank=True)
    serial_number = models.CharField(max_length=400, blank=True)
    container_acquisition_date = models.DateField(null=True, blank=True)
    container_warranty_bool = models.BooleanField(default = False)
    container_warranty_expiration_date = models.DateField(null=True, blank=True)
    group_owner = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    # Custom properties
    
    # Property which returns the number of days until expiration.
        # Note that negitive numbers mean days since expiration
    @property
    def days_until_warranty_expiration(self):
        # Expiration date 
        DaysDelta = self.container_warranty_expiration_date - date.today()
        
        return DaysDelta.days


    class Meta:
        ordering = ['site','container']
        permissions = (
            ("can_create_container_object_instance", "Create new container object instances"),
            ("can_update_container_object_instance", "Update existing container object instances"),
            ("can_delete_container_object_instance", "Delete existing container object instances"),
        )
        
    def get_absolute_url(self):
        """Returns the url to access a particular container instance."""
        return reverse('container-detail', args=[str(self.id)])
        
    def get_container_items_url(self):
        """Returns the url to access a particular container instance's items list."""
        return reverse('container-items', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.container.name})'



# Tier 4 models -- at least 1 tier 3 upstream relationship

# item_object_instance model
class item_object_instance(models.Model):
    """Model representing a specific copy of an item_object."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular item across the entire account.')
    item_object_instance_nickname = models.CharField(max_length=100, blank=False, default="my-item")
    # item = models.ForeignKey(item_object, on_delete=models.RESTRICT, null=True)
    item = models.ForeignKey(item_object, on_delete=models.SET_NULL, null=True)
    container_instance = models.ForeignKey(container_object_instance, on_delete=models.SET_NULL, null=True)
    # source = models.ForeignKey(acquisition_source, blank=True, on_delete=models.RESTRICT, null=True)
    source = models.ForeignKey(acquisition_source, blank=True, on_delete=models.SET_NULL, null=True)
    package_count = models.IntegerField(default = 1, null=True)
    number_in_package_count = models.IntegerField(default = 1, null=True)
    location_in_container = models.CharField(max_length=200, blank=True)
    item_acquisition_date = models.DateField(null=True, blank=True)
    item_deep_storage = models.BooleanField(default = False)
    item_expiration_date = models.DateField(null=True, blank=True)
    group_owner = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)


    # Custom properties
    
    # Property which returns the number of days until expiration.
        # Note that negitive numbers mean days since expiration
    @property
    def days_until_item_expiration(self):
        # Expiration date 
        DaysDelta = self.item_expiration_date - date.today()
        
        return DaysDelta.days



    class Meta:
        ordering = ['container_instance', 'item']
        
        permissions = (
            ("can_create_item_object_instance", "Create new item object instances"),
            ("can_update_item_object_instance", "Update existing item object instances"),
            ("can_delete_item_object_instance", "Delete existing item object instances"),
        )

    def get_absolute_url(self):
        """Returns the url to access a particular item instance."""
        return reverse('item-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.item.name})'


# Tier x models -- ...

# z
