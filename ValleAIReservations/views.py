from ValleAIReservations.models import Reserva
from ValleAIReservations.models import Table
from ValleAIReservations.serializer import TableSerializer
from ValleAIReservations.serializer import ReservaSerializer
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

class ReservaViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [isAdminOrCreateOnly]
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer


class TableViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Table.objects.all()
    serializer_class = TableSerializer