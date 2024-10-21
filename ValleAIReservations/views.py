from ValleAIReservations.models import Table, BookedTable, Reserva
from ValleAIReservations.serializer import TableSerializer, ReservaSerializer, BookedTableSerializer
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission, IsAdminUser

#Permissão criada para liberar as requisições GET e POST para todos os Usuários, e os métodos PUT e DELETE, somente para Admin
class isAdminOrCreateOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'POST']:
            return True
        if request.method in ['PUT', 'DELETE']:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_authenticated and request.user.is_staff

#Permissão criada para liberar somente a requisição de GET para usuários Gerais, enquanto as outras somente para Admin
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
