from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['get'])
    def context_contacts(self, request, pk=None):
        contact = self.get_object()
        context_contacts = ContextContact.objects.filter(contact=contact)
        serializer = ContextContactSerializer(context_contacts, many=True)
        return Response(serializer.data)
class ContextContactViewSet(viewsets.ModelViewSet):
    queryset = ContextContact.objects.all()
    serializer_class = ContextContactSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['contact', 'context', 'function', 'emailadress', 'telephone', 'postaladdress', 'parking_info']