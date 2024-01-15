import datetime
import time
from django import forms # Django's built-in high level forms code
from django.forms import ModelForm # Built-in form class when only a single model is being manipulated in a form
from django.core.exceptions import ValidationError # Used for raising data validation errors (E.g. raise ValidationError(...))
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, get_user_model, password_validation # Authentication code

# Add imports here
from core.models import site_type, address_type, item_object_instance, custom_user, user_registration_code

class AddressTypeForm(ModelForm):
    class Meta:
        model = address_type
        fields = ['name','location_country','location_locality','location_city',\
        'location_zipcode','location_address_line_1','location_address_line_2']

    
    # Override default form
    def __init__(self, *args, **kwargs):
       super(AddressTypeForm, self).__init__(*args, **kwargs)
       
       # Set default name field to prevent form submission lock
       self.initial['name'] = "My site address"


class SiteTypeForm(ModelForm):

    # Define checkbox bool    
    new_address_needed = forms.BooleanField(required=False, label='New address needed?')

    class Meta:
        model = site_type
        fields = ['name', 'site_address']


class QuickAddItemToContainerItemsList(ModelForm):
    class Meta:
        model = item_object_instance
        # Nickname gets user input, container_instance and item are required and will get place holders
        # fields = ['item_object_instance_nickname','container_instance','item']
        fields = ['item_object_instance_nickname','package_count']

# class UserRegistrationForm(ModelForm):
#     class Meta:
#         model = custom_user
#         fields = ['email', 'password']

# Copied the double password stuff and extra validations from Django org - 
    # https://github.com/django/django/blob/main/django/contrib/auth/forms.py#L10
class UserRegistrationForm(ModelForm):
    
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )
    
    # Define checkbox bool    
    # join_existing_group = forms.BooleanField(required=False, label='Join existing group?')
    
    class Meta:
        model = custom_user
        fields = ('email',)
        
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)


class UserRegistrationCodeForm(ModelForm):
   
    error_messages = {
        'bad_regcode': _('The registration code entered is not valid.'),
    }

    def clean_registration_code(self):
        registration_code = self.cleaned_data['registration_code']
        
        # Create a user_registration_code object to evaluate against
        userRegistrationCodeIteration = user_registration_code.objects.filter(registration_code__exact=registration_code).first()
        
        if userRegistrationCodeIteration is None:
            raise ValidationError(
                self.error_messages['bad_regcode'],
                code='bad_regcode',
            )
            
        return registration_code
    
    class Meta:
        model = user_registration_code
        fields = ['registration_code']
        
    # clean_<field name> is required
    # "clean" as a function name will catch everything
    # def clean_registration_code(self):
    #     super(UserRegistrationCodeForm, self).clean()
        
    #     user_registration_code = self.cleaned_data.get('registration_code')
        
    #     if len(user_registration_code) > 1:
    #         raise ValidationError(
    #             self.error_messages['bad_regcode'],
    #             code='bad_regcode',
    #         )
            
    #     return self.cleaned_data
