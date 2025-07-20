from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from hr.models import Employee, Department, Position, Attendance, LeaveRequest
from resorts.models import Resort
from accounts.models import User
import csv
import datetime
from django.contrib import messages
from django.db.models import Q
from .models import Payslip, Employee
from accounting.models import Category, Transaction

def employee_list(request):
    search_query = request.GET.get("search")
    export_type = request.GET.get("export")

    employees = Employee.objects.select_related("user", "resort", "department", "position")

    if search_query:
        employees = employees.filter(
            user__first_name__icontains=search_query
        ) | employees.filter(department__name__icontains=search_query)

    if export_type == "csv":
        return export_employee_csv(employees)
    elif export_type == "excel":
        # Optional: implement Excel export
        pass
    elif export_type == "pdf":
        # Optional: implement PDF export
        pass

    context = {
        "employees": employees,
        "users": User.objects.all(),
        "resorts": Resort.objects.all(),
        "departments": Department.objects.all(),
        "positions": Position.objects.all(),
    }
    return render(request, "hr/hr.html", context)

from django.contrib import messages


def save_employee(request):
    if request.method == "POST":
        try:
            emp_id = request.POST.get("id")
            user_id = request.POST.get("user")
            resort_id = request.POST.get("resort")
            department_id = request.POST.get("department")
            position_id = request.POST.get("position")
            date_joined = request.POST.get("date_joined")
            salary = request.POST.get("salary")
            is_active = request.POST.get("is_active") == "True"

            user = get_object_or_404(User, id=user_id)
            resort = get_object_or_404(Resort, id=resort_id)
            department = get_object_or_404(Department, id=department_id)
            position = get_object_or_404(Position, id=position_id)

            if emp_id:
                emp = get_object_or_404(Employee, id=emp_id)
                emp.user = user
                emp.resort = resort
                emp.department = department
                emp.position = position
                emp.date_joined = date_joined
                emp.salary = salary
                emp.is_active = is_active
                emp.save()
                messages.success(request, "✅ Employee updated successfully.")
            else:
                Employee.objects.create(
                    user=user,
                    resort=resort,
                    department=department,
                    position=position,
                    salary=salary,
                    date_joined=date_joined,
                    is_active=is_active
                )
                messages.success(request, "Employee added successfully.")

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return redirect("employee_list")


@login_required
def delete_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    emp.delete()
    return redirect("employee_list")


def export_employee_csv(employees):
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="employees_{}.csv"'.format(datetime.datetime.now().strftime("%Y%m%d"))

    writer = csv.writer(response)
    writer.writerow(["Full Name", "Resort", "Department", "Position", "Date Joined", "Status"])

    for emp in employees:
        writer.writerow([
            emp.user.get_full_name(),
            emp.resort.name,
            emp.department.name,
            emp.position.title,
            emp.date_joined,
            "Active" if emp.is_active else "Inactive"
        ])
    return response

def department_list(request):
    search = request.GET.get('search', '')
    departments = Department.objects.filter(name__icontains=search) if search else Department.objects.all()
    resorts = Resort.objects.all()

    if request.method == 'POST':
        dept_id = request.POST.get('id')
        name = request.POST['name']
        resort_id = request.POST['resort']
        resort = get_object_or_404(Resort, id=resort_id)

        if dept_id:
            department = get_object_or_404(Department, id=dept_id)
            department.name = name
            department.resort = resort
            department.save()
        else:
            Department.objects.create(name=name, resort=resort)

        return redirect('department_list')

    return render(request, 'hr/department_list.html', {'departments': departments, 'resorts': resorts})

def delete_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == 'POST':
        department.delete()
    return redirect('department_list')

def position_list(request):
    search_query = request.GET.get('search', '')
    positions = Position.objects.select_related('department')

    if search_query:
        positions = positions.filter(
            Q(title__icontains=search_query) | Q(department__name__icontains=search_query)
        )

    if request.method == "POST":
        pos_id = request.POST.get("id")
        title = request.POST.get("title")
        department_id = request.POST.get("department")

        department = get_object_or_404(Department, id=department_id)

        if pos_id:
            pos = get_object_or_404(Position, id=pos_id)
            pos.title = title
            pos.department = department
            pos.save()
            messages.success(request, "Position updated successfully.")
        else:
            Position.objects.create(title=title, department=department)
            messages.success(request, "Position added successfully.")
        return redirect('position_list')

    if request.GET.get("export") == "csv":
        # Export CSV logic (optional)
        pass

    departments = Department.objects.all()
    return render(request, "hr/position_list.html", {
        "positions": positions,
        "departments": departments,
        "search": search_query,
    })

def delete_position(request, id):
    pos = get_object_or_404(Position, id=id)
    pos.delete()
    messages.success(request, "Position deleted successfully.")
    return redirect('position_list')

def attendance_list(request):
    search = request.GET.get('search', '')
    attendances = Attendance.objects.select_related('employee')

    if search:
        attendances = attendances.filter(
            Q(employee__name__icontains=search) | Q(remarks__icontains=search)
        )

    if request.method == "POST":
        att_id = request.POST.get("id")
        emp_id = request.POST.get("employee")
        att_date = request.POST.get("date")
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        remarks = request.POST.get("remarks", "")

        employee = get_object_or_404(Employee, id=emp_id)

        if att_id:
            attendance = get_object_or_404(Attendance, id=att_id)
            attendance.employee = employee
            attendance.date = att_date
            attendance.check_in = check_in
            attendance.check_out = check_out
            attendance.remarks = remarks
            attendance.save()
            messages.success(request, "Attendance updated successfully.")
        else:
            exists = Attendance.objects.filter(employee=employee, date=att_date).exists()
            if exists:
                messages.warning(request, f"Attendance already recorded for {employee} on {att_date}.")
            else:
                Attendance.objects.create(
                    employee=employee,
                    date=att_date,
                    check_in=check_in,
                    check_out=check_out,
                    remarks=remarks
                )
                messages.success(request, "Attendance added successfully.")
        return redirect('attendance_list')

    employees = Employee.objects.all()
    return render(request, 'hr/attendance_list.html', {
        'attendances': attendances,
        'employees': employees,
        'search': search
    })


def delete_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    attendance.delete()
    messages.success(request, "Attendance deleted successfully.")
    return redirect('attendance_list')


def payslip_list(request):
    search = request.GET.get('search', '')
    payslips = Payslip.objects.select_related('employee__user', 'employee__resort')

    if search:
        payslips = payslips.filter(
            Q(employee__user__first_name__icontains=search) |
            Q(employee__user__last_name__icontains=search) |
            Q(employee__resort__name__icontains=search)
        )

    employees = Employee.objects.select_related('user', 'resort')

    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        payment_date_str = request.POST.get('payment_date')
        bonus = request.POST.get('bonus') or 0
        deductions = request.POST.get('deductions') or 0

        try:
            payment_date = datetime.datetime.strptime(payment_date_str, "%Y-%m-%d").date()
        except Exception:
            messages.error(request, "Invalid payment date format.")
            return redirect('payslip_list')

        employee = get_object_or_404(Employee, id=employee_id)
        salary = employee.salary
        bonus = float(bonus)
        deductions = float(deductions)
        net_pay = float(salary) + bonus - deductions

        # Check for duplicate payslip on same payment_date for employee
        if Payslip.objects.filter(employee=employee, payment_date=payment_date).exists():
            messages.warning(request, f"Payslip for {employee.user.email} on {payment_date} already exists.")
            return redirect('payslip_list')

        payslip = Payslip.objects.create(
            employee=employee,
            salary=salary,
            bonus=bonus,
            deductions=deductions,
            net_pay=net_pay,
            payment_date=payment_date,
            remarks=""
        )

        # Create accounting transaction
        salary_category, _ = Category.objects.get_or_create(name='Salary', type='expense')
        Transaction.objects.create(
            user=employee.user,
            category=salary_category,
            amount=net_pay,
            description=f'Salary payment on {payment_date}',
            date=payment_date
        )

        messages.success(request, f"Payslip generated for {employee.user.get_full_name()} on {payment_date}.")
        return redirect('payslip_list')

    context = {
        'payslips': payslips.order_by('-payment_date'),
        'employees': employees,
    }
    return render(request, 'hr/payslip_list.html', context)

@login_required
def save_payslip(request):
    if request.method == 'POST':
        employee_id = request.POST.get('employee_id')
        np_date = request.POST.get('np_date')  # e.g. '2082-03-01'

        if not np_date:
            messages.error(request, "Please select month and year.")
            return redirect('payslip_list')

        # Parse np_date, format: 'YYYY-MM-DD'
        try:
            year, month, _ = np_date.split('-')
            month = int(month)
            year = int(year)
        except Exception:
            messages.error(request, "Invalid date format.")
            return redirect('payslip_list')

        employee = get_object_or_404(Employee, id=employee_id)
        amount = employee.salary

        payslip_exists = Payslip.objects.filter(
            employee=employee,
            month=month,
            year=year
        ).exists()

        if payslip_exists:
            messages.warning(request, f"Payslip for {employee.user.get_full_name()} in {month}-{year} already exists.")
            return redirect('payslip_list')

        payslip = Payslip.objects.create(
            employee=employee,
            month=month,
            year=year,
            amount=amount
        )

        salary_category, _ = Category.objects.get_or_create(name='Salary', type='expense')
        Transaction.objects.create(
            user=employee.user,
            category=salary_category,
            amount=amount,
            description=f'Salary for {month}-{year}',
            date=datetime.date.today()
        )

        messages.success(request, f"Payslip created and salary recorded for {employee.user.get_full_name()} ({month}-{year}).")

    return redirect('payslip_list')

@login_required
def delete_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    payslip.delete()
    messages.success(request, "Payslip deleted successfully.")
    return redirect('payslip_list')