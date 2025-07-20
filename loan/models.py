from django.db import models
from django.contrib.auth.models import User

class Borrower(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_loan(self):
        return sum(loan.amount for loan in self.loans.all())

    def total_paid(self):
        return sum(p.amount for p in self.payments.all())

    def balance(self):
        return self.total_loan() - self.total_paid()

    def __str__(self):
        return self.name


class Loan(models.Model):
    borrower = models.ForeignKey(Borrower, related_name='loans', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    issue_date = models.DateField()
    due_date = models.DateField()

    def __str__(self):
        return f"Loan of NPR {self.amount} to {self.borrower.name}"


class Payment(models.Model):
    borrower = models.ForeignKey(Borrower, related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField()

    def __str__(self):
        return f"Payment of NPR {self.amount} by {self.borrower.name}"


class Notification(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.borrower.name}"
