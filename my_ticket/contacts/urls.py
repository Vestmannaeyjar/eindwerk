from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/create', views.contact_create, name='contact_create'),
    path('contacts/<int:contact_id>', views.contact_detail, name='contact_detail'),
    path('contacts/<int:contact_id>/delete/', views.contact_delete, name='contact_delete'),
    path('contacts/<int:contact_id>/update/', views.contact_update, name='contact_update'),
    path('contacts/<int:contact_id>/context/create/', views.contextcontact_create, name='contextcontact_create'),
    path('contacts/context/<int:contextcontact_id>/delete/', views.contextcontact_delete, name='contextcontact_delete'),
    path('contacts/context/<int:contextcontact_id>/update/', views.contextcontact_update, name='contextcontact_update'),
    path('contacts/<int:contact_id>/contextcontact/create/<int:address_id>/', views.contextcontact_create, name='contextcontact_create'),
    path('addresses/', views.address_list, name='address_list'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/contact/<int:contact_id>/create/', views.address_create, name='address_create_with_contact'),
    path('addresses/<int:address_id>/delete/', views.address_delete, name='address_delete'),
    path('addresses/<int:address_id>/update/', views.address_update, name='address_update'),
]
