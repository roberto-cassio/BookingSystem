from rest_framework import serializers
from ValleAIReservations.models import Reserva, Table, BookedTable


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'name', 'phone', 'num_people', 'datetime', 'status', 'waitlist_position']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'size']

class BookedTableSerializer(serializers.ModelSerializer):
    booking_id = serializers.PrimaryKeyRelatedField(queryset=Reserva.objects.all(), source='booking')
    mesa_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='mesa')
    class Meta:
        model = BookedTable
        fields = ['id', 'end_date','mesa_id', 'booking_id']