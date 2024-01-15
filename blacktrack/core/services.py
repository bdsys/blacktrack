# core app services
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

# Model imports
from .models import container_object_instance, item_object_instance, container_object, site_type, \
address_type, item_object, custom_user, user_registration_code, group_roster

# Form imports
from core.forms import AddressTypeForm, SiteTypeForm, QuickAddItemToContainerItemsList, UserRegistrationForm, UserRegistrationCodeForm


def GetUserContextGroupMembershipId(request):
    # Get a user's session using auth middleware
    userEmailContext = request.user
    userContext = custom_user.objects.filter(email__exact=userEmailContext).first()
    sessionContext = request.session
    
    print(f"userContext: {userContext}")
    print(f"sessionContext: {sessionContext}")
    
    # Preferred group handler
    
    # Set flag
    userContextHasGroupContext = False
    
    # Get all groups the user is a member of
    userContextGroupMemberships = userEmailContext.groups.all().first()
    
    print(f"userContextGroupMemberships: {userContextGroupMemberships}")
    
    if userContextGroupMemberships is None:
        userContextHasGroupContext = True
        # Landing will display a special message for users without a group membership,
        # prompting them to get one before doing anything else
        viewGroupContext = None
        
    try:
        if request.session["pref_group"]:
            # Validate that user has access to this group
            # Check group_roster WHERE group_id is requested session
                # AND custom_user_id is userContext's Id
                    # AND group_status isn't "p" for pending
            userContextGroupStatus = group_roster.objects.filter(
                group_id__id__exact=request.session["pref_group"]).filter(
                    custom_user_id__id__exact=userContext.id).exclude(
                        group_status__exact="p")
                        
            # If user passes validation, then they can proceed with preferred group.
            if userContextGroupStatus:
                userContextHasGroupContext = True
                viewGroupContext = request.session["pref_group"]
                
    # Catch error indicating that the session value does not exist and continue
    except KeyError:
        print("KeyError pass")
        pass
        
    # If user either has no session value on GET or they failed the preferred validation, 
    # then we'll go through each group in list order and assign the first one that the user 
    # passes a validation check on
    if userContextHasGroupContext == False:
        print("last userContextHasGroupContext is false invoked")
        
        # Either iterate through all group memberships or validate just the one membership
        try:
            print("Iterating through memberships to assign first come validation")
            for userContextGroupMembership in userContextGroupMemberships:
                userContextGroupStatus = group_roster.objects.filter(
                    group_id__id__exact=userContextGroupMembership.id).filter(
                        custom_user_id__id__exact=userContext.id).exclude(
                            group_status__exact="p")
                
                # Assign if the first group that the user passes validation against
                if userContextGroupStatus:
                    request.session["pref_group"] = userContextGroupMembership.id
                    userContextHasGroupContext = True
                    break
        except TypeError:
            print("Checking the one membership to assign first come validation")
            userContextGroupStatus = group_roster.objects.filter(
                group_id__id__exact=userContextGroupMemberships.id).filter(
                    custom_user_id__id__exact=userContext.id).exclude(
                        group_status__exact="p")
            
            # Assign if the first group that the user passes validation against
            if userContextGroupStatus:
                request.session["pref_group"] = userContextGroupMemberships.id
                viewGroupContext = request.session["pref_group"]
                userContextHasGroupContext = True
        
        if userContextHasGroupContext == False:
            # All group validations failed, this user needs to go get a group membership
            # Landing will display a special message for users without a group membership,
            # prompting them to get one before doing anything else
            print("All group membership validations failed. Going back to landing.")
            viewGroupContext = None
        else:
            viewGroupContext = request.session["pref_group"]
            
    print("User passed group membership validation with pref_group value: ")
    print(viewGroupContext)
    
    return viewGroupContext