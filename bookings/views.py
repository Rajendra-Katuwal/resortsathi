from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect,  get_object_or_404
from inventory.models import InventoryItem
from bookings.models import Booking, BookingStatus
from resorts.models import *
from rooms.models import RoomType, Room
from accounts.models import User
import csv
import io
import datetime
import openpyxl
from django.http import HttpResponse
from django.utils.dateparse import parse_date
from nepali_datetime import date as nep_date, datetime as nep_datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.utils.text import slugify

# Create your views here.
def booking(request):
    bookings = Booking.objects.select_related('room', 'resort').all()

    if request.method == "POST":
        room_id = request.POST.get("room")
        resort_id = request.POST.get("resort")
        check_in = request.POST.get("check-in")
        check_out = request.POST.get("check-out")
        total_price = request.POST.get("total-price")
        status = request.POST.get("status")

        Booking.objects.create(
            user=request.user,
            resort_id=resort_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            total_price=total_price,
            status=status
        )
        return redirect("booking")

    # Export logic
    export = request.GET.get("export")
    if export == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="room_bookings.csv"'
        writer = csv.writer(response)
        writer.writerow(["Room", "Check In", "Check Out", "Total Price", "Status"])
        for b in bookings:
            writer.writerow([b.room.name, b.check_in, b.check_out, b.total_price, b.status])
        return response

    elif export == "excel":
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="room_bookings.xls"'
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Bookings')

        columns = ["Room", "Check In", "Check Out", "Total Price", "Status"]
        for col_num in range(len(columns)):
            ws.write(0, col_num, columns[col_num])

        for row_num, b in enumerate(bookings, 1):
            ws.write(row_num, 0, b.room.name)
            ws.write(row_num, 1, str(b.check_in))
            ws.write(row_num, 2, str(b.check_out))
            ws.write(row_num, 3, float(b.total_price))
            ws.write(row_num, 4, b.status)

        wb.save(response)
        return response

    elif export == "pdf":
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="room_bookings.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)

        y = 750
        p.drawString(100, y, "Room Bookings")
        y -= 20

        for b in bookings:
            p.drawString(100, y, f"Room: {b.room.name} | {b.check_in} to {b.check_out} | NPR {b.total_price} | {b.status}")
            y -= 15

        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    context = {
        "page_title": "Room Booking",
        "table_headers": ["Room", "Check In", "Check Out", "Total Price", "Status"],
        "table_rows": [
                [b.room.name, b.check_in, b.check_out, b.total_price, b.get_status_display()] for b in bookings
            ],
        "form_fields": [
            {"label": "Room", "name": "room", "type": "select", "choices": Room.objects.all()},
            {"label": "Resort", "name": "resort", "type": "select", "choices": Resort.objects.all()},
            {"label": "Check In","class": "nepali-datepicker","name": "check-in", "type": "date"},
            {"label": "Check Out", "class": "nepali-datepicker","name": "check-out", "type": "nepali-date"},
            {"label": "Total Price", "name": "total-price", "type": "text"},
            {"label": "Status", "name": "status", "type": "select", "choices": BookingStatus.choices},
        ],
    }
    return render(request, "bookings/booking.html", context)

def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.delete()
    return redirect("booking")
def export_csv(bookings):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=bookings.csv"
    writer = csv.writer(response)
    writer.writerow(["Room", "Check In", "Check Out", "Total Price", "Status"])
    for b in bookings:
        writer.writerow([b.room.name, b.check_in, b.check_out, b.total_price, b.get_status_display()])
    return response

def export_excel(bookings):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["Room", "Check In", "Check Out", "Total Price", "Status"])
    for b in bookings:
        ws.append([b.room.name, str(b.check_in), str(b.check_out), float(b.total_price), b.get_status_display()])
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="bookings.xlsx"'
    wb.save(response)
    return response

def export_pdf(bookings):
    # Placeholder - PDF generation (e.g., ReportLab or WeasyPrint)
    response = HttpResponse("PDF generation not implemented yet", content_type="text/plain")
    return response
