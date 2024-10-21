from django.test import TestCase
from unittest.mock import patch, MagicMock
from ValleAIReservations.models import Reserva, BookedTable, Table
from django.utils import timezone

class ReservaTests(TestCase):
#TestCase para o Waitlist quando as mesas estiverem vazias.
    @patch('ValleAIReservations.models.BookedTable.objects.filter')
    @patch('ValleAIReservations.models.Table.objects.count')
    def test_create_reserva_when_tables_are_full(self, mock_table_count, mock_booked_tables_filter):
        mock_table_count.return_value = 2  

        mock_booked_tables = MagicMock()  
        mock_booked_tables.count.return_value = 2  
        mock_booked_tables_filter.return_value = mock_booked_tables  
        for i in range(5):
            response = self.client.post('/reservations/', {
                'name': f'Test User {i + 1}',
                'phone': f'12345678{i}',  
                'num_people': 4,
                'datetime': timezone.now()
            })

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['status'], 'e') 
            self.assertIsNotNone(response.data['waitlist_position'])

            new_reserva = Reserva.objects.get(id=response.data['id'])
            new_reserva.refresh_from_db()

            waitlist_count = Reserva.objects.filter(status='e').count()
            print("WaitList Count após a criação:", waitlist_count)
            print(f"Reserva criada (Mesas Ocupadas) {i + 1}:", response.data)

#TestCase para o Waitlist caso as mesas estiverem cheias
    @patch('ValleAIReservations.models.BookedTable.objects.filter')
    @patch('ValleAIReservations.models.Table.objects.count')
    def test_create_reserva_when_tables_are_available(self, mock_table_count, mock_booked_tables_filter):
        mock_table_count.return_value = 2  

        mock_booked_tables = MagicMock()  
        mock_booked_tables.count.return_value = 0  
        mock_booked_tables_filter.return_value = mock_booked_tables  

       
        for i in range(5):  
            response = self.client.post('/reservations/', {
                'name': f'Test User {i + 1}',
                'phone': f'12345678{i}',
                'num_people': 4,
                'datetime': timezone.now()  
            })

            
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['status'], 'c')  
            self.assertIsNone(response.data['waitlist_position'])

            print(f"Reserva criada {i + 1}:", response.data)
