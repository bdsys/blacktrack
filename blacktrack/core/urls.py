from django.urls import path, re_path
from . import views

urlpatterns = [
    
    # /core/warmup
    path('warmup/', views.warmup, name='warmup'),
    
    # /core/index.html
    path('', views.index, name='index'),
    
    # /core/landing.html
    path('landing/', views.AuthorizedLanding, name='landing'),
    
    # /core/registeruser
    path('registeruser/', views.UserRegistrationFunction, name="user-registration"),
    
    # /core/items
    path('items/', views.listAllItems, name='list-items'),
    # /core/containers
    path('containers/', views.listAllContainers, name='list-containers'),
    
    # /core/containers-session
    path('containers-session/', views.listAllContainersSession, name='list-containers-session'),
    
    # /core/container/<id>
    path('container/<uuid:pk>', views.ContainerDetailView.as_view(), name='container-detail'),
    # /core/item/<id>
    path('item/<uuid:pk>', views.ItemDetailView.as_view(), name='item-detail'),
    # /core/container-items/<id>
    # path('container-items/<uuid:pk>', views.ContainerItemsView.as_view(), name='container-items'),
    # custom /core/container-items/<id>
    # Note <uuid:pk> is shorthand for pattern matching of a UUID - <uuid:var>
        # E.g. path('container-items/<uuid:pk>', views.ContainerItemsView, name='container-items'), - var pased to view is "pk"
    path('container-items/<uuid:ContainerInstanceUuid>', views.ContainerItemsView, name='container-items'),
    
    # address_type paths
    # /core/addresses
    path('addresses/', views.AddressListView.as_view(), name='list-addresses'),
    # /core/address/<id>
    path('address/<int:pk>', views.AddressDetailView.as_view(), name='address-detail'),
    # /core/address/create
    path('address/create/', views.AddressCreate.as_view(), name='address-create'),
    # /core/address/<address_id>/update
    path('address/<int:pk>/update/', views.AddressUpdate.as_view(), name='address-update'),
    # /core/address/<address_id>/delete
    path('address/<int:pk>/delete/', views.AddressDelete.as_view(), name='address-delete'),
    
    
    # site_type paths
    # /core/sites
    path('sites/', views.SiteListView.as_view(), name='list-sites'),
    # /core/site/<id>
    path('site/<int:pk>', views.SiteDetailView.as_view(), name='site-detail'),
    # /core/site/create
    # path('site/create/', views.SiteCreate.as_view(), name='site-create'),
    path('site/create/', views.SiteCreateFunction, name='site-create'),
    # /core/site/<site_id>/update
    path('site/<int:pk>/update/', views.SiteUpdate.as_view(), name='site-update'),
    # /core/site/<site_id>/delete
    path('site/<int:pk>/delete/', views.SiteDelete.as_view(), name='site-delete'),
    
]
