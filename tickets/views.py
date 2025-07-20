import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .utils import generate_ticket_pdf
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse

from .models import Ticket, TicketTemplate, TicketCounter
from .forms import TicketForm
from crm.models import CorporateCustomer, OrganizationCustomer
from accounting.models import Transaction, Category

@login_required
def ticket_list_view(request):
    walkin_tickets = Ticket.objects.filter(customer_type__isnull=True, customer_id__isnull=True)
    corporate_type = ContentType.objects.get_for_model(CorporateCustomer)
    org_type = ContentType.objects.get_for_model(OrganizationCustomer)

    corporate_tickets = Ticket.objects.filter(customer_type=corporate_type)
    organization_tickets = Ticket.objects.filter(customer_type=org_type)

    context = {
        'walkin_tickets': walkin_tickets,
        'corporate_tickets': corporate_tickets,
        'organization_tickets': organization_tickets,
        'ticket_templates': TicketTemplate.objects.all(),
        'ticket_counters': TicketCounter.objects.all(),
        'corporate_customers': CorporateCustomer.objects.all(),
        'organization_customers': OrganizationCustomer.objects.all(),
    }
    return render(request, 'tickets/ticket_list.html', context)

@login_required
def issue_ticket(request):
    if request.method == 'POST':
        ticket_type = request.POST.get('ticket_type')  # walkin, corporate, organization
        customer_id_raw = request.POST.get('customer_id')
        try:
            customer_id = int(customer_id_raw) if customer_id_raw else None
        except ValueError:
            customer_id = None


        form = TicketForm(request.POST)

        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.issued_by = request.user

            if ticket_type == 'corporate' and customer_id:
                ct = ContentType.objects.get_for_model(CorporateCustomer)
                ticket.customer_type = ct
                ticket.customer_id = customer_id
            elif ticket_type == 'organization' and customer_id:
                ct = ContentType.objects.get_for_model(OrganizationCustomer)
                ticket.customer_type = ct
                ticket.customer_id = customer_id
            
            category, _ = Category.objects.get_or_create(name="Ticket", type="income")
            transaction = Transaction.objects.create(
                user = request.user,
                category=category,
                amount=ticket.total_price,
                description=f"Ticket issued: {ticket.ticket_id}",
                date=timezone.now()
            )
            print(transaction)
            ticket.save()
            print("TICKET SAVED:", ticket.ticket_id, ticket.customer_type, ticket.customer_id)

            messages.success(request, f'{ticket_type.capitalize()} ticket issued successfully!')
        else:
            messages.error(request, 'Ticket issuance failed. Please check your input.')

    return redirect(f"{reverse('tickets:ticket-list')}")


@login_required
def delete_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.delete()
    messages.success(request, 'Ticket deleted successfully.')
    return redirect('tickets:ticket-list')


@login_required
def print_ticket_view(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    filename = f"ticket_{ticket.ticket_id}.pdf"  # UUID for unique file naming
    pdf_relative_path = f"tickets/{filename}"
    pdf_full_path = os.path.join(settings.MEDIA_ROOT, pdf_relative_path)
    pdf_url = os.path.join(settings.MEDIA_URL, pdf_relative_path)

    if not os.path.exists(pdf_full_path):
        data_list = [{
            'ticket_id': str(ticket.ticket_id),
            'template_name': ticket.template.name,
            'issued_at': ticket.issued_at.strftime('%Y-%m-%d'),
            'copy_no': i + 1,
            'total': ticket.quantity
        } for i in range(ticket.quantity)]

        pdf_buffer = generate_ticket_pdf(ticket, data_list)
        os.makedirs(os.path.dirname(pdf_full_path), exist_ok=True)
        with open(pdf_full_path, 'wb') as f:
            f.write(pdf_buffer.getbuffer())

    if os.path.exists(pdf_full_path):
        full_url = request.build_absolute_uri(pdf_url)
        return JsonResponse({'pdf_url': full_url})
    else:
        return JsonResponse({'error': 'PDF generation failed.'}, status=500)
    

# COUNTERS

@login_required
def counter_list_view(request):
    counters = TicketCounter.objects.all()
    return render(request, 'tickets/counter_list.html', {'counters': counters})

@login_required
def counter_create_or_edit(request, pk=None):
    instance = get_object_or_404(TicketCounter, pk=pk) if pk else None

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        location = request.POST.get('location', '').strip()

        if not name:
            messages.error(request, 'Counter name is required.')
            return redirect('tickets:counter-list')

        if not instance and TicketCounter.objects.filter(name=name).exists():
            messages.error(request, 'Counter with this name already exists.')
            return redirect('tickets:counter-list')

        if instance:
            instance.name = name
            instance.location = location
            instance.save()
            messages.success(request, 'Counter updated.')
        else:
            TicketCounter.objects.create(name=name, location=location)
            messages.success(request, 'Counter created.')

        return redirect('tickets:counter-list')

    return redirect('tickets:counter-list')

@login_required
def counter_delete(request, pk):
    counter = get_object_or_404(TicketCounter, pk=pk)
    counter.delete()
    messages.success(request, 'Counter deleted.')
    return redirect('tickets:counter-list')

# TEMPLATES

@login_required
def template_list_view(request):
    templates = TicketTemplate.objects.all()
    return render(request, 'tickets/template_list.html', {'templates': templates})

@login_required
def template_create_or_edit(request, pk=None):
    instance = get_object_or_404(TicketTemplate, pk=pk) if pk else None
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        if instance:
            instance.name = name
            instance.price = price
            instance.description = description
            instance.save()
            messages.success(request, 'Template updated.')
        else:
            TicketTemplate.objects.create(name=name, price=price, description=description)
            messages.success(request, 'Template created.')
        return redirect('tickets:template-list')
    return redirect('tickets:template-list')

@login_required
def template_delete(request, pk):
    template = get_object_or_404(TicketTemplate, pk=pk)
    template.delete()
    messages.success(request, 'Template deleted.')
    return redirect('tickets:template-list')
