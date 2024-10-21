INSERT INTO ValleAIReservations_table (size, name, created_by, created_at) VALUES 
(4, 'Mesa 1', 'admin', NOW()),
(4, 'Mesa 2', 'admin', NOW()),
(6, 'Mesa 3', 'admin', NOW()),
(2, 'Mesa 4', 'admin', NOW()),
(8, 'Mesa 5', 'admin', NOW()),
(4, 'Mesa 6', 'admin', NOW()),
(6, 'Mesa 7', 'admin', NOW()),
(4, 'Mesa 8', 'admin', NOW()),
(2, 'Mesa 9', 'admin', NOW()),
(6, 'Mesa 10', 'admin', NOW()),
(8, 'Mesa 11', 'admin', NOW()),
(4, 'Mesa 12', 'admin', NOW()),
(6, 'Mesa 13', 'admin', NOW()),
(2, 'Mesa 14', 'admin', NOW());

INSERT INTO ValleAIReservations_reserva (name, phone, num_people, datetime, status, created_by, created_at) VALUES
('João Silva', '555-1234', 4, '2024-10-22 19:00:00', 'c', 'admin', NOW()),
('Maria Oliveira', '555-5678', 2, '2024-10-22 20:00:00', 'e', 'admin', NOW()),
('Pedro Souza', '555-8765', 6, '2024-10-22 19:30:00', 'c', 'admin', NOW()),
('Ana Costa', '555-4321', 3, '2024-10-22 21:00:00', 'e', 'admin', NOW());

INSERT INTO ValleAIReservations_bookedtable (booking_id, mesa_id, end_date) VALUES
(1, 1, '2024-10-22 21:00:00'),
(1, 2, '2024-10-22 21:00:00'),
(2, 3, '2024-10-22 21:00:00'),
(3, 4, '2024-10-22 21:00:00'),
(3, 5, '2024-10-22 21:00:00'),
(4, 6, '2024-10-22 21:00:00'),
(4, 7, '2024-10-22 21:00:00'),
(1, 8, '2024-10-22 21:00:00'),
(2, 9, '2024-10-22 21:00:00'),
(3, 10, '2024-10-22 21:00:00'),
(4, 11, '2024-10-22 21:00:00'),
(1, 12, '2024-10-22 21:00:00'),
(2, 13, '2024-10-22 21:00:00'),
(3, 14, '2024-10-22 21:00:00');
