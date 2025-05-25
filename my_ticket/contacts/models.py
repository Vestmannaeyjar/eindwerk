from django.db import models
import datetime


class Address(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.street}, {self.zip} {self.city}, {self.country} ({self.name})"


class Contact(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    date_of_birth = models.DateField(default=datetime.date.today)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class ContextContact(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    context = models.CharField(max_length=255)
    function = models.CharField(max_length=255)
    emailaddress = models.EmailField(max_length=255)
    telephone = models.CharField(max_length=30)
    postaladdress = models.ForeignKey(Address, on_delete=models.CASCADE)
    parking_info = models.TextField()

    def __str__(self):
        return f"{self.contact} - {self.context}"

