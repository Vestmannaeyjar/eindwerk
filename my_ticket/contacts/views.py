from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from .models import Contact
from .forms import ContactForm


def contact_list(request):
    query = request.GET.get('q')  # 'q' is the name of the input field in the form
    contacts = Contact.objects.all().order_by('firstname','lastname')

    if query:
        contacts = contacts.filter(
            Q(firstname__icontains=query) | Q(lastname__icontains=query) | Q(date_of_birth__icontains=query)
        )
    return render(request, 'contacts/list.html', {'contacts': contacts, 'query': query})


def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_list')  # Make sure your URL name matches
    else:
        form = ContactForm()
    return render(request, 'contacts/new.html', {'form': form})


def contact_update(request, contact_id):
    # Get the contact object based on the provided ID, or return a 404 if not found
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
