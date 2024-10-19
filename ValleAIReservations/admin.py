from django.contrib import admin

from ValleAIReservations.models import Reserva, Table, BookedTable


class Reservas(admin.ModelAdmin):
    list_display = ('id','name', 'phone','num_people', 'datetime')
    list_display_link = ('id', 'name')

class Tables(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')

class BookedTables(admin.ModelAdmin):
    list_display = ('id', 'end_date', 'booking_id', 'mesa_id') 
    list_display_link = ('id')

admin.site.register(Reserva, Reservas)
admin.site.register(Table,Tables)
admin.site.register(BookedTable, BookedTables)
