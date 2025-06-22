from rest_framework import filters, viewsets
from .models import Address, Contact, ContextContact
from .serializers import AddressSerializer, ContactSerializer, ContextContactSerializer


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'street', 'city', 'zip', 'country']


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['firstname', 'lastname', 'date_of_birth']


class ContextContactViewSet(viewsets.ModelViewSet):
    queryset = ContextContact.objects.all()
    serializer_class = ContextContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['contact', 'context', 'function', 'emailadress', 'telephone', 'postaladdress', 'parking_info']