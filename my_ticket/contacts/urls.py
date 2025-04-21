from django.urls import path
from . import views

urlpatterns = [
    path('contacts/', views.contact_list, name='contact_list'),
    path('contacts/new', views.contact_create, name='contact_create'),
    path('<int:contact_id>/delete/', views.contact_delete, name='contact_delete'),
    path('<int:contact_id>/update/', views.contact_update, name='contact_update'),
]
