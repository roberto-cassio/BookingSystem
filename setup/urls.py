from django.contrib import admin
from django.urls import path, include
from ValleAIReservations.views import ReservaViewSet, TableViewSet, BookedTablesViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('reservations', ReservaViewSet, basename='Reservas')
router.register('seats', TableViewSet, basename='Tables' )
router.register('bookedtables',BookedTablesViewSet, basename="BookedTables" )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(router.urls))
]
