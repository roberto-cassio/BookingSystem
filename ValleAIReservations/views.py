from ValleAIReservations.models import Table, BookedTable, Reserva
from ValleAIReservations.serializer import TableSerializer, ReservaSerializer, BookedTableSerializer
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission, IsAdminUser


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

    def create(self, request, *args, **kwargs):
        booked_tables = BookedTable.objects.filter(end_date__isnull=True).count()
        total_tables = Table.objects.count()

        if booked_tables >= total_tables:
            request.data['status'] = 'e'
            wailist_count = Reserva.objects.filter(status='e').count()
            request.data['waitlist_position'] = wailist_count + 1
        else:
            request.data['status'] = 'c'
            request.data['waitlist_position'] = None
 
        return super().create(request,*args,**kwargs)
    
    def move_from_waitlist(self):
        waitlist_next =  Reserva.objects.filter(status='e').order_by('waitlist_position').first()
        if waitlist_next:
            waitlist_next.status = 'c'
            waitlist_next.waitlist_position = None
            waitlist_next.save()
    
    def update(self,request,*args,**kwargs):
        booking = self.get_object()

        if request.user.is_staff:
            new_status = request.data.get('status')
            if new_status in ['c', 'e']:
                booking.status = new_status
                booking.save()

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