from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import CorporateCustomer, OrdinaryCustomer, OrganizationCustomer
from .forms import CorporateCustomerForm, OrdinaryCustomerForm, OrganizationCustomerForm


def customer_list(request):
    corporate_customers = CorporateCustomer.objects.all()
    ordinary_customers = OrdinaryCustomer.objects.all()
    organization_customers = OrganizationCustomer.objects.all()

    search = request.GET.get('search')
    if search:
        corporate_customers = corporate_customers.filter(company_name__icontains=search)
        ordinary_customers = ordinary_customers.filter(full_name__icontains=search)
        organization_customers = organization_customers.filter(organization_name__icontains=search)

    return render(request, 'crm/customer_list.html', {
        'corporate_customers': corporate_customers,
        'ordinary_customers': ordinary_customers,
        'organization_customers': organization_customers,
        'page_title': 'All Customers',
    })


def corporate_customer_form(request, pk=None):
    instance = get_object_or_404(CorporateCustomer, pk=pk) if pk else None
    form = CorporateCustomerForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Corporate Customer saved.")
        else:
            messages.error(request, "Please fix errors and try again.")
        return redirect('crm:customer_list')  # always redirect to main page

    # For GET requests, just redirect to customer list (no separate form page)
    return redirect('crm:customer_list')


def ordinary_customer_form(request, pk=None):
    instance = get_object_or_404(OrdinaryCustomer, pk=pk) if pk else None
    form = OrdinaryCustomerForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Ordinary Customer saved.")
        else:
            messages.error(request, "Please fix errors and try again.")
        return redirect('crm:customer_list')

    return redirect('crm:customer_list')


def organization_customer_form(request, pk=None):
    instance = get_object_or_404(OrganizationCustomer, pk=pk) if pk else None
    form = OrganizationCustomerForm(request.POST or None, request.FILES or None, instance=instance)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Organization Customer saved.")
        else:
            messages.error(request, "Please fix errors and try again.")
        return redirect('crm:customer_list')

    return redirect('crm:customer_list')


def delete_customer(request, customer_type, pk):
    model_map = {
        'corporate': CorporateCustomer,
        'ordinary': OrdinaryCustomer,
        'organization': OrganizationCustomer
    }
    model = model_map.get(customer_type)
    if not model:
        messages.error(request, "Invalid customer type.")
        return redirect('crm:customer_list')

    instance = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        instance.delete()
        messages.success(request, "Customer deleted.")
        return redirect('crm:customer_list')

    # No fallback delete confirmation page; redirect to main list
    messages.error(request, "Delete action not confirmed.")
    return redirect('crm:customer_list')
