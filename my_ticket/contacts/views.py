from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Address, Contact, ContextContact
from .forms import AddressForm, ContactForm, ContextContactForm


def contact_list(request):
    query = request.GET.get('q')  # 'q' is the name of the input field in the form
    contacts = Contact.objects.all().order_by('firstname', 'lastname')

    if query:
        contacts = contacts.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(date_of_birth__icontains=query)
        )
    contacts = contacts.annotate(num_context_contacts=Count('contextcontact'))

    paginator = Paginator(contacts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contacts/list.html', {'page_obj': page_obj, 'query': query})


def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/new.html', {'form': form})


def contact_update(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == "POST":
        form = ContactForm(request.POST, instance=contact)
        if form.is_valid():
            form.save()
            return redirect('contact_list')
    else:
        form = ContactForm(instance=contact)

    return render(request, 'contacts/update.html', {'form': form, 'contact': contact})


def contact_delete(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    if request.method == 'POST':
        contact.delete()
        return redirect('contact_list')

    return render(request, 'contacts/delete.html', {'contact': contact})


def contact_detail(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)

    context_contacts = contact.contextcontact_set.all()

    return render(request, 'contacts/detail.html', {
        'contact': contact,
        'context_contacts': context_contacts
    })


def contextcontact_create(request, contact_id, address_id=None):
    contact = get_object_or_404(Contact, id=contact_id)

    initial_data = {}
    if address_id:
        address = get_object_or_404(Address, id=address_id)
        initial_data['postaladdress'] = address

    if request.method == 'POST':
        form = ContextContactForm(request.POST)
        if form.is_valid():
            new_context_contact = form.save(commit=False)
            new_context_contact.contact = contact  # ensure link to contact
            form.save()
            return redirect('contact_detail', contact_id=contact.id)
    else:
        form = ContextContactForm(initial=initial_data)

    return render(request, 'contacts/new_context.html', {
        'form': form,
        'contact': contact
    })


def contextcontact_delete(request, contextcontact_id):
    contextcontact = get_object_or_404(ContextContact, id=contextcontact_id)

    if request.method == 'POST':
        contextcontact.delete()
        return redirect('contact_detail', contact_id=contextcontact.contact.id)

    return render(request, 'contacts/delete_context.html', {'contextcontact': contextcontact})


def contextcontact_update(request, contextcontact_id):
    contextcontact = get_object_or_404(ContextContact, id=contextcontact_id)
    contact = contextcontact.contact  # Get the associated Contact
    address = contextcontact.postaladdress  # Get the current postal address if any

    if request.method == 'POST':
        form = ContextContactForm(request.POST, instance=contextcontact)
        if form.is_valid():
            updated_context_contact = form.save(commit=False)
            updated_context_contact.contact = contact  # Ensure it is still linked to the correct Contact
            if 'address' in request.POST:
                new_address = get_object_or_404(Address, id=request.POST['address'])
                updated_context_contact.postaladdress = new_address  # Update the postal address if provided
            updated_context_contact.save()
            return redirect('contact_detail', contact_id=contact.id)
    else:
        form = ContextContactForm(instance=contextcontact)

    return render(request, 'contacts/update_context.html', {'form': form, 'contextcontact': contextcontact, 'address': address, 'contact': contact})


def address_create(request, contextcontact_id=None, contact_id=None):
    contextcontact = get_object_or_404(ContextContact, id=contextcontact_id) if contextcontact_id else None
    contact = get_object_or_404(Contact, id=contact_id) if contact_id else None

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            new_address = form.save()

            if contextcontact:
                contextcontact.postaladdress = new_address
                contextcontact.save()

                return redirect('contact_detail', contextcontact.contact.id)
            elif contact:
                return redirect('contextcontact_create', contact_id=contact.id, address_id=new_address.id)
            else:
                return redirect('address_list')
    else:
        form = AddressForm()

    return render(request, 'contacts/new_address.html', {
        'form': form,
        'contextcontact': contextcontact,
        'contact': contact,
    })


def address_list(request):
    query = request.GET.get('q')
    addresses = Address.objects.all().order_by('street', 'city')

    if query:
        addresses = addresses.filter(
            Q(name__icontains=query) | Q(street__icontains=query) | Q(city__icontains=query) | Q(zip__icontains=query) | Q(country__icontains=query)
        )

    paginator = Paginator(addresses, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contacts/list_addresses.html', {'page_obj': page_obj, 'query': query})


def address_delete(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if request.method == 'POST':
        address.delete()
        return redirect('address_list')

    return render(request, 'contacts/delete_address.html', {'address': address})


def address_update(request, address_id):
    address = get_object_or_404(Address, id=address_id)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('address_list')
    else:
        form = AddressForm(instance=address)

    return render(request, 'contacts/update_address.html', {'form': form, 'address': address})

