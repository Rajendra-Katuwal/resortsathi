from django.shortcuts import render, redirect, get_object_or_404
from rooms.models import RoomType, Room
from resorts.models import Resort
from django.http import HttpResponse
import csv
import openpyxl
from io import BytesIO
from reportlab.pdfgen import canvas
# Create your views here.
def room_type(request):
    queryset = RoomType.objects.all()
    search = request.GET.get("search")

    if search:
        queryset = queryset.filter(name__icontains=search)

    export_type = request.GET.get("export")
    if export_type == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="room_types.csv"'
        writer = csv.writer(response)
        writer.writerow(['Name', 'Description'])
        for obj in queryset:
            writer.writerow([obj.name, obj.description])
        return response

    elif export_type == "excel":
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Name', 'Description'])
        for obj in queryset:
            sheet.append([obj.name, obj.description])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="room_types.xlsx"'
        workbook.save(response)
        return response

    elif export_type == "pdf":
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="room_types.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        y = 800
        p.drawString(100, y, 'Room Types')
        y -= 20
        for obj in queryset:
            p.drawString(100, y, f"{obj.name} - {obj.description}")
            y -= 20
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    if request.method == "POST":
        obj_id = request.POST.get("id")
        name = request.POST.get("type")
        description = request.POST.get("description")
        if obj_id:
            obj = RoomType.objects.get(id=obj_id)
            obj.name = name
            obj.description = description
            obj.save()
        else:
            RoomType.objects.create(name=name, description=description)
        return redirect("room_type")

    context = {
        "page_title": "Room Types",
        "table_headers": ["Type", "Description"],
        "table_rows": [[obj.name, obj.description, obj.id] for obj in queryset]
    }
    return render(request, "rooms/room_type.html", context)

def delete_room_type(request, pk):
    obj = get_object_or_404(RoomType, pk=pk)
    obj.delete()
    return redirect("room_type")



def room(request):
    queryset = Room.objects.select_related('resort', 'room_type').all()
    search = request.GET.get("search")

    if search:
        queryset = queryset.filter(name__icontains=search)

    export_type = request.GET.get("export")
    if export_type == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="rooms.csv"'
        writer = csv.writer(response)
        writer.writerow(['Resort', 'Room Type', 'Name', 'Description', 'Price/Night', 'Max Guests', 'Available'])
        for obj in queryset:
            writer.writerow([
                obj.resort.name,
                obj.room_type.name if obj.room_type else '',
                obj.name,
                obj.description,
                obj.price_per_night,
                obj.max_guests,
                "Yes" if obj.is_available else "No",
            ])
        return response

    elif export_type == "excel":
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.append(['Resort', 'Room Type', 'Name', 'Description', 'Price/Night', 'Max Guests', 'Available'])
        for obj in queryset:
            sheet.append([
                obj.resort.name,
                obj.room_type.name if obj.room_type else '',
                obj.name,
                obj.description,
                obj.price_per_night,
                obj.max_guests,
                "Yes" if obj.is_available else "No",
            ])
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="rooms.xlsx"'
        workbook.save(response)
        return response

    elif export_type == "pdf":
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="rooms.pdf"'
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        y = 800
        p.drawString(100, y, 'Rooms')
        y -= 20
        for obj in queryset:
            p.drawString(100, y, f"{obj.resort.name} - {obj.name} - {obj.room_type.name if obj.room_type else ''}")
            y -= 20
        p.showPage()
        p.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    if request.method == "POST":
        obj_id = request.POST.get("id")
        resort_id = request.POST.get("resort")
        room_type_id = request.POST.get("room_type")
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        guests = request.POST.get("max_guests")
        available = request.POST.get("status") == "true"  # from select field

        if obj_id:
            room = get_object_or_404(Room, pk=obj_id)
            room.resort_id = resort_id
            room.room_type_id = room_type_id
            room.name = name
            room.description = description
            room.price_per_night = price
            room.max_guests = guests
            room.is_available = available
            room.save()
        else:
            Room.objects.create(
                resort_id=resort_id,
                room_type_id=room_type_id,
                name=name,
                description=description,
                price_per_night=price,
                max_guests=guests,
                is_available=available
            )
        return redirect("room")

    context = {
        "page_title": "Rooms",
        "table_headers": ["Resort", "Room Type", "Name", "Price/Night", "Max Guests", "Available"],
        "table_rows": [[
            r.resort.name,
            r.room_type.name if r.room_type else '',
            r.name,
            r.price_per_night,
            r.max_guests,
            "Yes" if r.is_available else "No",
            r.id,
            r.description or '',
            r.resort.id,
            r.room_type.id if r.room_type else '',
            "true" if r.is_available else "false",
        ] for r in queryset],
        "resorts": Resort.objects.all(),
        "room_types": RoomType.objects.all(),
    }
    return render(request, "rooms/room.html", context)

def delete_room(request, pk):
    get_object_or_404(Room, pk=pk).delete()
    return redirect("room")