import json # used for creating JSON objects
import sys # used for exception handling
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic # Generic classes for lists and details of individual models
from django.views.generic.edit import CreateView, UpdateView, DeleteView # Generic classes for form creation of individual models
from django.contrib.auth import login, authenticate
from django.contrib.auth.hashers import make_password
from django.urls import reverse, reverse_lazy

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

# "Require logins" code for function based views
# DB permissions for function based views 
from django.contrib.auth.decorators import login_required, permission_required

# "Require logins" code for class based views, like generics
# DB permissions for class based views 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Django base models
from django.contrib.auth.models import Group

# Core app services
from .services import GetUserContextGroupMembershipId

# Model imports
from .models import container_object_instance, item_object_instance, container_object, site_type, \
address_type, item_object, custom_user, user_registration_code, group_roster

# Form imports
from core.forms import AddressTypeForm, SiteTypeForm, QuickAddItemToContainerItemsList, UserRegistrationForm, UserRegistrationCodeForm

# /core/warmup

def warmup(request):
    "Gets an app server server and database ready for work"
    
    if request.method == 'GET':
        print("Starting warmup...")
        
        responseJson = {}
        routineJson = {}
        dbInitJson = {}
        
        responseJson['status'] = "ERROR"
        responseJson['status-reason'] = "N/A"
        
        
        print("Starting db-init routine...")
        
        routineJson['routine-name'] = "db-init"
        
        print("Querying for quick-add item_object...")
        # .fist() executes the QuerySet and returns None is nothing matches
        ItemObjectInstanceQuickAdd = item_object.objects.filter(name__exact="quick-add").first()
        
        if ItemObjectInstanceQuickAdd:
            
            print("Found!")
            
            dbInitStatus = "OK"
            dbInitStatusReason = "object-exists"
        else:
            
            print("Not found, trying to create...")
            
            try:
                item_object.objects.create(name = "quick-add")
                print("Created!")
                
                dbInitStatus = "OK"
                dbInitStatusReason = "object-created"
                
            except:
                print("Error during warmup -- db-init routine!")
                
                dbInitStatus = "ERROR"
                dbInitStatusReason = sys.exc_info()[0]
            
        dbInitJson['status'] = dbInitStatus
        dbInitJson['status-reason'] = dbInitStatusReason
    
        # Set reponse to OK if code makes it to the end
        responseJson['status'] = "OK"
        responseJson['status-reason'] = "warmup-complete"
        
        responseJson['routine'] = routineJson
        routineJson['db-init'] = dbInitJson
    
        # print(json.dumps(responseJson))
    
        return HttpResponse(json.dumps(responseJson), content_type="application/json")


# /core/index.html
def index(request):
    """View function for anonymous splash page."""
    
    if request.user.is_authenticated == True:
        return HttpResponseRedirect(reverse('landing'))

    else:    
        # Place all container_object_instance's into an arr and another var that count's the them
        container_object_instance_arr = container_object_instance.objects.all()
        number_of_container_object_instance = container_object_instance_arr.count()
        
        container_object_instance_arr = item_object_instance.objects.all()
        number_of_item_object_instance = container_object_instance_arr.count()
    
        # Number of vists to the site from a specific cookie
        num_visits = request.session.get('num_visits_cookie_list', 0) # Get cookie "num_visits_cookie_list', if non-existant create new and set to 0
        request.session['num_visits_cookie_list'] = num_visits + 1
    
        # Python dictionary data array
        context = {
            'number_of_container_object_instance': number_of_container_object_instance,
            'number_of_item_object_instance': number_of_item_object_instance,
        }
    
        # Render the HTML template index.html with the data in the context variable
        return render(request, 'index.html', context=context)
    

# /core/landing.html
def AuthorizedLanding(request):
    """View function for authorized splash page."""
    
    if request.user.is_authenticated == False:
        return HttpResponseRedirect(reverse('index'))
        # return redirect(reverse('index'))

    
    else:
    
        # Place all container_object_instance's into an arr and another var that count's the them
        container_object_instance_arr = container_object_instance.objects.all()
        number_of_container_object_instance = container_object_instance_arr.count()
        
        container_object_instance_arr = item_object_instance.objects.all()
        number_of_item_object_instance = container_object_instance_arr.count()
    
        # Number of vists to the site from a specific cookie
        num_visits = request.session.get('num_visits_cookie_list', 0) # Get cookie "num_visits_cookie_list', if non-existant create new and set to 0
        request.session['num_visits_cookie_list'] = num_visits + 1
    
        # Python dictionary data array
        context = {
            'number_of_container_object_instance': number_of_container_object_instance,
            'number_of_item_object_instance': number_of_item_object_instance,
        }
    
        # Render the HTML template index.html with the data in the context variable
        return render(request, 'landing.html', context=context)

# /core/containers
@ login_required
def listAllContainers(request):
    """View function for container listing and management"""
    
    # Place all container_object_instance's into an arr and another var that count's the them
    container_object_instance_arr = container_object_instance.objects.all()
    number_of_container_object_instance = container_object_instance_arr.count()

    # for each loop that counts the number of item_object_instances in each container_object_instance
    # container_object_instance_item_count_arr = []
    listOfContainersAndItemCount = []
    
    for container_object_instance_object in container_object_instance_arr:

        temp_item_count = item_object_instance.objects.filter(container_instance__id__exact=container_object_instance_object.id).count()
        # container_object_instance_item_count_arr.append(temp_item_count)

        sublist = []
        sublist.append(container_object_instance_object.container_object_instance_nickname)
        sublist.append(temp_item_count)
        sublist.append(container_object_instance_object.get_absolute_url)
        sublist.append(container_object_instance_object.get_container_items_url)
        listOfContainersAndItemCount.append(sublist)
        

    # Python dictionary data array
    context = {
        # 'container_object_instance_arr': container_object_instance_arr,
        'number_of_container_object_instance': number_of_container_object_instance,
        # 'container_object_instance_item_count_arr': container_object_instance_item_count_arr,
        'listOfContainersAndItemCount': listOfContainersAndItemCount,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'list_containers.html', context=context)
    
    
### Sessions test


# /core/containers-session
@ login_required
def listAllContainersSession(request):
    """View function for container listing and management"""

    viewGroupContext = GetUserContextGroupMembershipId(request)
    
    print("viewGroupContext: ")
    print(viewGroupContext)
    
    if viewGroupContext is None:
        print("Group membership validations failed, returning to landing...")
        return HttpResponseRedirect(reverse('landing'))
        
    print("User passed group membership validation with pref_group value: ")
    print(viewGroupContext)
    
    
        
    # Place all container_object_instance's into an arr and another var that count's the them
    container_object_instance_arr = container_object_instance.objects.filter(group_owner_id__id__exact=viewGroupContext).all()
    
    if container_object_instance_arr:
        number_of_container_object_instance = container_object_instance_arr.count()
    else:
        container_object_instance_arr = []
        number_of_container_object_instance = 0

    # for each loop that counts the number of item_object_instances in each container_object_instance
    # container_object_instance_item_count_arr = []
    listOfContainersAndItemCount = []
    
    for container_object_instance_object in container_object_instance_arr:

        temp_item_count = item_object_instance.objects.filter(container_instance__id__exact=container_object_instance_object.id).count()
        # container_object_instance_item_count_arr.append(temp_item_count)

        sublist = []
        sublist.append(container_object_instance_object.container_object_instance_nickname)
        sublist.append(temp_item_count)
        sublist.append(container_object_instance_object.get_absolute_url)
        sublist.append(container_object_instance_object.get_container_items_url)
        listOfContainersAndItemCount.append(sublist)
        

    # Python dictionary data array
    context = {
        # 'container_object_instance_arr': container_object_instance_arr,
        'number_of_container_object_instance': number_of_container_object_instance,
        # 'container_object_instance_item_count_arr': container_object_instance_item_count_arr,
        'listOfContainersAndItemCount': listOfContainersAndItemCount,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'list_containers.html', context=context)


###
    
  
# /core/items/
@ login_required
def listAllItems(request):
    """View function for items-by-container listing and management"""

    # Place all container_object_instance's into an arr and another var that count's the them
    item_object_instance_arr = item_object_instance.objects.all()
    
    # Python dictionary data array
    context = {
        'item_object_instance_arr': item_object_instance_arr,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'list_items.html', context=context)



# /core/container/<container id>
class ContainerDetailView(LoginRequiredMixin, generic.DetailView):
    """View function for viewing details of individual container"""

    model = container_object_instance
    paginate_by = 20
    
    
# /core/item/<container id> # TODO
class ItemDetailView(LoginRequiredMixin, generic.DetailView):
    """View function for viewing details of individual item"""
    
    model = item_object_instance
    paginate_by = 5

# /core/container-items/<container id>
@ login_required
def ContainerItemsView(request, ContainerInstanceUuid):
    """View function for viewing details of individual container"""

    # Database queries
    ContainerObjectInstance = container_object_instance.objects.get(pk=ContainerInstanceUuid)
    # Alt method of getting container object instance to auto 404
    ContainerObjectInstance404 = get_object_or_404(container_object_instance, pk=ContainerInstanceUuid)
    ItemObjectInstanceQuickAdd = item_object.objects.filter(name__exact="quick-add").first()

    ContainerObjectInstanceItems = item_object_instance.objects.filter(container_instance__id__exact=ContainerInstanceUuid)

    
    # HTTP POST form behavior
    if request.method == 'POST': # Form has been submitted
        itemObjectInstanceQuickAddForm = QuickAddItemToContainerItemsList(request.POST, prefix = "item_object_instance_quickadd")
        
        if itemObjectInstanceQuickAddForm.is_valid():
            print ("itemObjectInstanceQuickAddForm validations passed for ContainerItemsView POST")
            
            item_object_instance_quickadd = itemObjectInstanceQuickAddForm.save(commit=False)
            
            # Insert the container object using context of the page itself, which would 404 without a single instance to use
            item_object_instance_quickadd.container_instance = ContainerObjectInstance404
                
            if ItemObjectInstanceQuickAdd:
                item_object_instance_quickadd.item = ItemObjectInstanceQuickAdd
            
            # Save to database with user input name, contextual container instance and default first entry of "quickadd" found in item_object table
            item_object_instance_quickadd.save()
            
            return HttpResponseRedirect(reverse('container-items', kwargs={'ContainerInstanceUuid':ContainerObjectInstance404.id}))
        
        else:
            print ("itemObjectInstanceQuickAddForm validations FAILED for ContainerItemsView POST")

    else:
        itemObjectInstanceQuickAddForm = QuickAddItemToContainerItemsList(prefix = "item_object_instance_quickadd")
        
        
    # Example, not for this function, specifically
    # temp_item_count = item_object_instance.objects.filter(container_instance__id__exact=container_object_instance_object.id).count()
    
    ListOfContainerItemsAndExpirationNegitiveReversals = []
    
    # For loop to create a list of [0] = item and [1] = negitive reversal
    for item in ContainerObjectInstanceItems:

        negitiveReverse = None

        if item.item_expiration_date:
            if item.days_until_item_expiration < 0:
                # E.g. -31 * -1 = 31
                negitiveReverse = item.days_until_item_expiration * -1
        
        sublist = []
        sublist.append(item)
        sublist.append(negitiveReverse)
        ListOfContainerItemsAndExpirationNegitiveReversals.append(sublist)
    
    
    # Return container instance and a list of items in instance [0] and a negitive number reverse [1]
    context = {
        'ContainerObjectInstance': ContainerObjectInstance,
        'ListOfContainerItemsAndExpirationNegitiveReversals': ListOfContainerItemsAndExpirationNegitiveReversals,
        'itemObjectInstanceQuickAddForm': itemObjectInstanceQuickAddForm,
    }
    
    return render(request, 'container-items.html', context=context)

# /core/addresses/
class AddressListView(LoginRequiredMixin,generic.ListView):
    model = address_type
    paginate_by = 20
    
# /core/address/<address_id>
class AddressDetailView(LoginRequiredMixin, generic.DetailView):
    """View function for viewing details of individual address"""
    model = address_type
    paginate_by = 20
    
# address_type pages
class AddressCreate(PermissionRequiredMixin, CreateView):
    model = address_type
    fields = ['name', 'location_country', 'location_locality', 'location_city', 'location_zipcode', \
    'location_address_line_1', 'location_address_line_2']
    
    # PermissionRequiredMixin parameters
    permission_required = 'core.can_create_address'

class AddressUpdate(PermissionRequiredMixin, UpdateView):
    model = address_type
    fields = ['name', 'location_country', 'location_locality', 'location_city', 'location_zipcode', \
    'location_address_line_1', 'location_address_line_2']
    
    # Renders to the same template as Create

    # PermissionRequiredMixin parameters
    permission_required = 'core.can_update_address'

class AddressDelete(PermissionRequiredMixin, DeleteView):
    model = address_type
    success_url = reverse_lazy('list-addresses') 
    
    # PermissionRequiredMixin parameters
    permission_required = 'core.can_delete_address'


# site_type pages
# /core/sites/
class SiteListView(LoginRequiredMixin,generic.ListView):
    model = site_type
    paginate_by = 20
    
# /core/site/<site_id>
class SiteDetailView(LoginRequiredMixin, generic.DetailView):
    """View function for viewing details of individual site"""
    model = site_type
    paginate_by = 20
    
class SiteCreate(PermissionRequiredMixin, CreateView):
    model = site_type
    fields = ['name', 'site_address']
    
    # PermissionRequiredMixin parameters
    permission_required = 'core.can_create_site'
    
    
@login_required
@permission_required('core.can_create_site', raise_exception=True)
def SiteCreateFunction(request):
    if request.method == 'POST': # Form has been submitted
        
        site_type_form = SiteTypeForm(request.POST, prefix = "site_type")

        # Proceed with site form processing regardlass of new address form input bool condition
        if site_type_form.is_valid():
            print ("site_type_form validations passed for SiteCreateFunction")
            site_type = site_type_form.save(commit=False) # Creates a model object, but doesn't commit to the database

        # Check if new address was input, my_var = dict.get(<key>, <default>)
        if request.POST.get('site_type-new_address_needed', False): # Checkbox value is None if not checked and "on" if checked
        
            address_type_form = AddressTypeForm(request.POST, prefix = "address_type")
            
            if address_type_form.is_valid():
                
                print ("address_type_form validations passed for SiteCreateFunction")
                
                address_type = address_type_form.save()
                site_type.site_address = address_type
            
            
        # Save site_type data and 302 to site list
        site_type.save()

        return HttpResponseRedirect(reverse('list-sites'))
        
    
    else:
        address_type_form = AddressTypeForm(prefix = "address_type")
        site_type_form = SiteTypeForm(prefix = "site_type")
    
    context = {
        'address_type_form': address_type_form,
        'site_type_form': site_type_form,
    }
    
    return render(request, "core/site_type_create_custom.html", context)
  

class SiteUpdate(PermissionRequiredMixin, UpdateView):
    model = site_type
    fields = ['name', 'site_address']
    
    # PermissionRequiredMixin parameters
    permission_required = 'core.can_update_site'

class SiteDelete(PermissionRequiredMixin, DeleteView):
    model = site_type
    success_url = reverse_lazy('list-sites') 
    
    # PermissionRequiredMixin parameters
    permission_required = 'core.can_delete_site'

# custom_user views
class CustomUserUpdate(PermissionRequiredMixin, UpdateView):
    model = custom_user
    fields = ['email', 'password']
    
    # Renders to the same template as Create

    # PermissionRequiredMixin parameters
    permission_required = 'core.can_update_custom_user'

def UserRegistrationFunction(request):
    
    # Unauthenticated users, only.
    if request.user.is_authenticated == True:
        return HttpResponseRedirect(reverse('landing'))
    
    if request.method == 'POST': # Form has been submitted
        
        custom_user_form = UserRegistrationForm(request.POST, prefix = "custom_user")
        user_registration_code_form = UserRegistrationCodeForm(request.POST, prefix = "user_registration_code")
        
        if custom_user_form.is_valid() and user_registration_code_form.is_valid():
            print ("custom_user_form and user_registration_code_form validations passed for UserRegistrationFunction")
            custom_user = custom_user_form.save(commit=False) # Creates a model object, but doesn't commit to the database
            
            if request.POST.get('custom_user-password2', False): # Ensures password2 is passed in properly, probably not needed since the form sanitizes that condition...
                email = custom_user.email
                password = request.POST.get('custom_user-password2', False)
                custom_user.set_password(password) # Sets password on model object using password hashing algorithm defined in settings.py
                
                # # Existing group membership form
                # if request.POST.get('custom_user-join_existing_group', False): # Checkbox value is None if not checked and "on" if checked
                #     print("user requesting to join existing group")
                    
                
                # Reg key counter for statistics on usage
                user_registration_code_object = user_registration_code_form.save(commit=False)
                userRegistrationCodeIteration = user_registration_code.objects.filter(registration_code__exact=user_registration_code_object.registration_code).first()

                iterationIncrease = userRegistrationCodeIteration.usage_counter + 1
                userRegistrationCodeIteration.usage_counter = iterationIncrease
                userRegistrationCodeIteration.save()

                # Commit new user to DB
                custom_user.save()
                
                # Authenticates the new user to the system after registration                    
                user = authenticate(username=email, password=password)
                login(request, user)
                login
                
                return HttpResponseRedirect(reverse('landing'))
                   
    else:
        custom_user_form = UserRegistrationForm(prefix = "custom_user")
        user_registration_code_form = UserRegistrationCodeForm(prefix = "user_registration_code")
    
    context = {
        'custom_user_form': custom_user_form,
        'user_registration_code_form': user_registration_code_form,
    }
    
    return render(request, "core/custom_user_create_custom.html", context)
