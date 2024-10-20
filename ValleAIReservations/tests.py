from django.test import TestCase
from unittest.mock import patch, MagicMock
from ValleAIReservations.models import Reserva, BookedTable, Table
from django.utils import timezone

class ReservaTests(TestCase):

    @patch('ValleAIReservations.models.BookedTable.objects.filter')
    @patch('ValleAIReservations.models.Table.objects.count')
    def test_create_reserva_when_tables_are_full(self, mock_table_count, mock_booked_tables_filter):
        # Simule a contagem de mesas
        mock_table_count.return_value = 2  # Suponha que existem 2 mesas disponíveis

        # Simule que todas as mesas estão ocupadas
        mock_booked_tables = MagicMock()  # Cria um objeto MagicMock para simular o queryset
        mock_booked_tables.count.return_value = 2  # Todas as mesas estão ocupadas
        mock_booked_tables_filter.return_value = mock_booked_tables  # Retorna o mock quando filter é chamado

        # Repetir a criação de reservas várias vezes
        for i in range(5):  # Altere o número para quantas vezes deseja repetir
            response = self.client.post('/reservations/', {
                'name': f'Test User {i + 1}',
                'phone': f'12345678{i}',
                'num_people': 4,
                'datetime': timezone.now()  # Usando timezone.now() para obter a data e hora atual com timezone
            })

            # Verifique se a reserva foi criada na lista de espera
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['status'], 'e')  # Espera
            self.assertIsNotNone(response.data['waitlist_position'])

            # Imprima o objeto da reserva criada
            print(f"Reserva criada {i + 1}:", response.data)

    @patch('ValleAIReservations.models.BookedTable.objects.filter')
    @patch('ValleAIReservations.models.Table.objects.count')
    def test_create_reserva_when_tables_are_available(self, mock_table_count, mock_booked_tables_filter):
        # Simule a contagem de mesas
        mock_table_count.return_value = 2  # Suponha que existem 2 mesas disponíveis

        # Simule que não há mesas ocupadas
        mock_booked_tables = MagicMock()  # Cria um objeto MagicMock para simular o queryset
        mock_booked_tables.count.return_value = 0  # Nenhuma mesa ocupada
        mock_booked_tables_filter.return_value = mock_booked_tables  # Retorna o mock quando filter é chamado

        # Repetir a criação de reservas várias vezes
        for i in range(5):  # Altere o número para quantas vezes deseja repetir
            response = self.client.post('/reservations/', {
                'name': f'Test User {i + 1}',
                'phone': f'12345678{i}',
                'num_people': 4,
                'datetime': timezone.now()  # Usando timezone.now() para obter a data e hora atual com timezone
            })

            # Verifique se a reserva foi criada e está confirmada
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data['status'], 'c')  # Confirmada
            self.assertIsNone(response.data['waitlist_position'])

            # Imprima o objeto da reserva criada
            print(f"Reserva criada {i + 1}:", response.data)
