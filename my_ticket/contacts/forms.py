from django import forms
from .models import Address, Contact, ContextContact


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class ContextContactForm(forms.ModelForm):
    class Meta:
        model = ContextContact
        fields = ['context', 'function', 'emailaddress', 'telephone', 'postaladdress', 'parking_info']
