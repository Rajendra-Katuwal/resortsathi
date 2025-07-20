from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Borrower, Loan, Payment, Notification
from django.db.models import Sum
from django.utils.timezone import now


def loan_dashboard(request):
    borrowers = Borrower.objects.all()
    loans = Loan.objects.select_related('borrower').all()
    payments = Payment.objects.select_related('borrower').all()
    recent_loans = loans.order_by('-issue_date')[:10]
    unread_notifications = Notification.objects.filter(is_read=False)

    context = {
        "total_borrowers": borrowers.count(),
        "total_loans": loans.aggregate(Sum('amount'))['amount__sum'] or 0,
        "total_payments": payments.aggregate(Sum('amount'))['amount__sum'] or 0,
        "recent_loans": recent_loans,
        "borrowers": borrowers,
        "notifications": unread_notifications,
    }
    return render(request, "loan/loan_dashboard.html", context)


def add_borrower(request):
    if request.method == "POST":
        name = request.POST.get("name")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        if name and contact and address:
            Borrower.objects.create(name=name, contact=contact, address=address)
            messages.success(request, "Borrower added successfully.")
        else:
            messages.error(request, "All fields are required.")
    return redirect("loan_dashboard")


def add_loan(request):
    if request.method == "POST":
        borrower_id = request.POST.get("borrower_id")
        amount = request.POST.get("amount")
        issue_date = request.POST.get("issue_date")
        due_date = request.POST.get("due_date")
        if borrower_id and amount and issue_date and due_date:
            Loan.objects.create(
                borrower_id=borrower_id,
                amount=amount,
                issue_date=issue_date,
                due_date=due_date
            )
            messages.success(request, "Loan issued successfully.")
        else:
            messages.error(request, "All fields are required.")
    return redirect("loan_dashboard")


def add_payment(request):
    if request.method == "POST":
        borrower_id = request.POST.get("borrower_id")
        amount = request.POST.get("amount")
        payment_date = request.POST.get("payment_date")
        if borrower_id and amount and payment_date:
            Payment.objects.create(
                borrower_id=borrower_id,
                amount=amount,
                payment_date=payment_date
            )
            messages.success(request, "Payment recorded successfully.")
        else:
            messages.error(request, "All fields are required.")
    return redirect("loan_dashboard")


def mark_notification_read(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    notif.is_read = True
    notif.save()
    messages.info(request, f"Marked notification {notif.id} as read.")
    return redirect("loan_dashboard")
