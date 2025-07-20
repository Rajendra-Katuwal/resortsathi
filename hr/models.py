from django.db import models
from django.conf import settings
from resorts.models import Resort

class Department(models.Model):
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.resort.name})"

class Position(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='positions')
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} - {self.department.name}"

class Employee(models.Model):
    GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    resort = models.ForeignKey(Resort, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateField()
    contact_number = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    certificate = models.ImageField(upload_to='certificates/', blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    taxpayer_id = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.user.email
    
class BankAccount(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_account')
    account_number = models.CharField(max_length=20, unique=True)
    bank_name = models.CharField(max_length=100)
    branch_name = models.CharField(max_length=100, blank=True)
    identifier_code = models.CharField(max_length=11, blank=True)
    bank_location = models.CharField(max_length=255, blank=True)
    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.account_number}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee} - {self.date}"

    class Meta:
        unique_together = ('employee', 'date')

class LeaveRequest(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status_choices = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee} | {self.start_date} to {self.end_date} | {self.status}"

class Payslip(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(auto_now_add=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.payment_date}"
