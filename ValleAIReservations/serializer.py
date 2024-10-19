from rest_framework import serializers
from ValleAIReservations.models import Reserva, Table, BookedTable


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'name', 'phone', 'num_people', 'datetime']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'size']

class BookedTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookedTable
        fields = ['id', 'end_date','mesa_id', 'booking_id']