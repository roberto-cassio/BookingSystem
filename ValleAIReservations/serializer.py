from rest_framework import serializers
from ValleAIReservations.models import Reserva, Table, BookedTable
from datetime import timedelta
from django.utils import timezone


class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = ['id', 'name', 'phone', 'num_people', 'datetime','waitlist_position', 'status']
    def create(self, validated_data):
        booked_tables = BookedTable.objects.filter(end_date__gt=timezone.now() + timedelta(hours=1)).count()
        total_tables = Table.objects.count()
        print(f'Booked Tables: {booked_tables} e Total Tables: {total_tables}')

        if booked_tables >= total_tables:
            print("All tables are booked, adding to the waitlist")
            waitlist_count = Reserva.objects.filter(status='e').count()
            validated_data['status'] = 'e'
            validated_data['waitlist_position'] = waitlist_count + 1
        else:
            print("There are available tables, confirming the reservation")
            validated_data['status'] = 'c'
            validated_data['waitlist_position'] = None

        return super().create(validated_data)
    

    def move_from_waitlist(self, validated_data):
        waitlist_reservations = Reserva.objects.filter(status='e').order_by('waitlist_position')
        if waitlist_reservations.exists():
            reservation_to_move = waitlist_reservations.first()
            reservation_to_move.status = 'c'
            reservation_to_move.waitlist_position = None
            reservation_to_move.save()
            print(f"Moved reservation {reservation_to_move.id} from waitlist to confirmed.")

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.num_people = validated_data.get('num_people', instance.num_people)
        instance.datetime = validated_data.get('datetime', instance.datetime)

        booked_tables = BookedTable.objects.filter(end_date__gt=timezone.now() + timedelta(hours=1)).count()
        total_tables = Table.objects.count()

        if booked_tables >= total_tables and instance.status != 'e':
            print("All tables are booked, moving to waitlist")
            instance.status = 'e'
            waitlist_count = Reserva.objects.filter(status='e').count()
            instance.waitlist_position = waitlist_count + 1
        elif booked_tables < total_tables and instance.status == 'e':
            print("There are available tables, confirming the reservation")
            instance.status = 'c'
            instance.waitlist_position = None
        
        instance.save()
        return instance

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