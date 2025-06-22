from rest_framework import serializers
from .models import Address, Contact, ContextContact


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ContextContactSerializer(serializers.ModelSerializer):
    contextcontact_firstname = serializers.CharField(source='contact.firstname', read_only=True)
    contextcontact_lastname = serializers.CharField(source='contact.lastname', read_only=True)
    contextcontact_name = serializers.SerializerMethodField()

    def get_contextcontact_name(self, obj):
        if obj.contact:
            firstname = obj.contact.firstname or ""
            lastname = obj.contact.lastname or ""
            function = obj.function or "onbekend"
            return f"{firstname} {lastname} ({function})".strip()
        return ""

    class Meta:
        model = ContextContact
        fields = '__all__'
