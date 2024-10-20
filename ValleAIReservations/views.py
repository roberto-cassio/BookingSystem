from datetime import timedelta
from django.utils import timezone
from ValleAIReservations.models import Table, BookedTable, Reserva
from ValleAIReservations.serializer import TableSerializer, ReservaSerializer, BookedTableSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission, IsAdminUser
from rest_framework.response import Response


class isAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        if request.method in ['PUT', 'DELETE']:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_staff


class isAdminOrReadOnly(BasePermission):
    def has_permission(self,request,view):
        if request.method == 'GET':
            return True
        else:
            return request.user and request.user.is_authenticated and request.user.is_staff
        
class ReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [isAdminOrCreateOnly]
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    
    def move_from_waitlist(self):
        waitlist_next =  Reserva.objects.filter(status='e').order_by('waitlist_position').first()
        if waitlist_next:
            waitlist_next.status = 'c'
            waitlist_next.waitlist_position = None
            waitlist_next.save()
    
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        duration = timedelta(hours = 1)
        
        booked_tables = BookedTable.objects.filter(end_date__gt=timezone.now()+duration).count()
        total_tables = Table.objects.count()
        print(data['name'])
        print(f'Booked Tables: {booked_tables}, Total Tables: {total_tables}')
        
        if booked_tables >= total_tables:
            print("All tables are booked, adding to the waitlist")
            data['status'] = 'e'
            waitlist_count = Reserva.objects.filter(status='e').count()
            print(f'Waitlist Type: {type(waitlist_count)}')
            data['waitlist_position'] = int(waitlist_count + 1)
        else:
            print("There are available tables, confirming the reservation")
            data['status'] = 'c'
            data['waitlist_position'] = None

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        print(serializer.errors)
        self.perform_create(serializer)

        self.move_from_waitlist()

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        waitlist_position = self.request.data.get('waitlist_position')

        if isinstance(waitlist_position, list):
            waitlist_position = waitlist_position[0]

        serializer.save(waitlist_position=16)

    def update(self,request,*args,**kwargs):
        booking = self.get_object()

        if request.user.is_staff:
            new_status = request.data.get('status')
            if new_status in ['c', 'e']:
                booking.status = new_status
                booking.save()

        self.move_from_waitlist()

        return super().update(request,*args,**kwargs)

class TableViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [isAdminOrReadOnly]
    queryset = Table.objects.all()
    serializer_class = TableSerializer


class BookedTablesViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = BookedTable.objects.all()
    serializer_class = BookedTableSerializer