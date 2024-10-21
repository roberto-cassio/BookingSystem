from rest_framework import serializers
from ValleAIReservations.models import Reserva, Table, BookedTable
from datetime import timedelta
from django.utils import timezone


class ReservaSerializer(serializers.ModelSerializer):
    #Definindo o modelo e os dados a serem serializados na Classe Meta
    class Meta:
        model = Reserva
        fields = ['id', 'name', 'phone', 'num_people', 'datetime','waitlist_position', 'status']
    #Função para sobrescrever o método create do FrameWork e adicionar a lógica de WaitList na adição de Equipamentos
    def create(self, validated_data):
        #Verificação se no momento atual, quantas mesas constam como agendadas em relação a quantidade de mesas disponíveis.
        booked_tables = BookedTable.objects.filter(end_date__gt=timezone.now()).count()
        total_tables = Table.objects.count()
        print(f'Booked Tables: {booked_tables} e Total Tables: {total_tables}')
        #Caso haja uma quantidade de mesas agendadas maior ou igual o de mesas totais, ele retorna como em espera, se não fica como confirmada.
        if booked_tables >= total_tables:
            print("All tables are booked, adding to the waitlist")
            waitlist_count = Reserva.objects.filter(status='e').count()
            validated_data['status'] = 'e'
            #Aqui soma um na contagem da Waitlist caso adicione mais alguém na espera.
            validated_data['waitlist_position'] = waitlist_count + 1
        else:
            print("There are available tables, confirming the reservation")
            validated_data['status'] = 'c'
            validated_data['waitlist_position'] = None

        return super().create(validated_data)

    #Método para mover a primeira reserva da Waitlist para Confirmado retirando a Waitlist position do mesmo
    def move_from_waitlist(self, validated_data):
        waitlist_reservations = Reserva.objects.filter(status='e').order_by('waitlist_position')
        if waitlist_reservations.exists():
            reservation_to_move = waitlist_reservations.first()
            reservation_to_move.status = 'c'
            reservation_to_move.waitlist_position = None
            reservation_to_move.save()
            print(f"Moved reservation {reservation_to_move.id} from waitlist to confirmed.")
            
    #Função para sobrescrever o método update do Framework para adicionar a lógica da wait_list
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.num_people = validated_data.get('num_people', instance.num_people)
        instance.datetime = validated_data.get('datetime', instance.datetime)

        booked_tables = BookedTable.objects.filter(end_date__gt=timezone.now()).count()
        total_tables = Table.objects.count()
        
        # Verifica se todas as mesas estão reservadas e se a reserva não está na lista de espera.
        if booked_tables >= total_tables and instance.status != 'e':
            print("All tables are booked, moving to waitlist")
            instance.status = 'e'
            waitlist_count = Reserva.objects.filter(status='e').count()
            instance.waitlist_position = waitlist_count + 1
         # Se houver mesas disponíveis e a reserva estiver na lista de espera, ela é confirmada.
        elif booked_tables < total_tables and instance.status == 'e':
            print("There are available tables, confirming the reservation")
            self.move_from_waitlist(validated_data)
            instance.status = 'c'
            instance.waitlist_position = None
        
        instance.save()
        return instance
#Serializer das mesas
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'name', 'size']
#Serializer das Mesas Agendadas
class BookedTableSerializer(serializers.ModelSerializer):
    #Serialização das chaves estrangeiras
    booking_id = serializers.PrimaryKeyRelatedField(queryset=Reserva.objects.all(), source='booking')
    mesa_id = serializers.PrimaryKeyRelatedField(queryset=Table.objects.all(), source='mesa')
    class Meta:
        model = BookedTable
        fields = ['id', 'end_date','mesa_id', 'booking_id']
