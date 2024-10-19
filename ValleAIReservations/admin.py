from django.contrib import admin

from ValleAIReservations.models import Reserva, Table


class Reservas(admin.ModelAdmin):
    list_display = ('id','name', 'phone','num_people', 'datetime')
    list_display_link = ('id', 'name')

class Tables(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_link = ('id', 'name')

admin.site.register(Reserva, Reservas)
admin.site.register(Table,Tables)

