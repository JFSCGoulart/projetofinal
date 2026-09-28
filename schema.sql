-- Dados iniciais
INSERT OR IGNORE INTO usuarios (id, nome, email, senha, turma, tipo)
VALUES (1, 'Coordenador Padrão', 'admin@qualifica.com',
'hash_admin', NULL, 'coordenador');
INSERT OR IGNORE INTO salas (nome, andar, capacidade, tipo) VALUES
('Sala 101', 1, 30, 'sala_aula'),
('Sala 102', 1, 30, 'sala_aula'),
('Sala 103', 1, 20, 'laboratorio'),
('Sala 201', 2, 40, 'sala_aula'),
('Sala 202', 2, 25, 'laboratorio'),
('Sala 203', 2, 30, 'sala_aula'),
('Sala 301', 3, 50, 'auditorio'),
('Sala 302', 3, 30, 'sala_aula'),
('Sala 401', 4, 100, 'auditorio'),
('Sala 402', 4, 25, 'reuniao');