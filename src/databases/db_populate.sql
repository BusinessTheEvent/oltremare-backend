-- Inserimento dati nella tabella school_grade
INSERT INTO public.school_grade (grade, price) VALUES 
('Elementari', 15.00),
('Medie', 18.00),
('Superiori', 22.00);

-- Inserimento dati nella tabella subjects
INSERT INTO public.subjects (name) VALUES 
('Inglese'),
('Spagnolo'),
('Tedesco'),
('Matematica'),
('Fisica'),
('Economia'),
('Chimica'),
('Diritto'),
('Latino'),
('Italiano'),
('Storia'),
('Geografia'),
('Geometria'),
('Scienze'),
('Arte e immagine'),
('Musica'),
('Francese'),
('Tecnologia');
    

-- ('Scienze'),
-- ('Storia'),
-- ('Geografia'),
-- ('Letteratura'),

-- ('Biologia'),
-- ('Arte'),
-- ('Musica'),
-- ('Educazione Fisica'),
-- ('Informatica'),

-- ('Filosofia'),
-- ('Sociologia'),
-- ('Psicologia'),
-- ('Scienze Politiche'),
-- ('Scienze Ambientali'),

-- ('Francese'),
-- ('Drammaturgia'),
-- ('Ingegneria'),
-- ('Scienze Aziendali'),
-- ('Statistica'),
-- ('Etica'),
-- ('Astronomia');

-- Inserimento dati nella tabella users
-- INSERT INTO public.users (username, name, surname, birthdate, password, is_active, disabled, registered_at, last_login, date_init_validity, date_end_validity) 
-- VALUES 

-- -- Utente che è chief
-- ('chief@prova.prova', 'Martina', 'Lucarda', '1995-08-08', 'password23', true, false, '2024-07-08 17:00:00', '2024-07-18 17:00:00', '2024-07-08 17:00:00', '2024-12-31 23:59:59'),

-- -- Utenti che sono insegnanti (teacher)
-- -- Insegnanti di lingue
-- ('Federica.M@prova.prova', 'Federica', 'M', '1990-01-01', 'password1', true, false, '2024-07-01 10:00:00', '2024-07-10 10:00:00', '2024-07-01 10:00:00', '2024-12-31 23:59:59'),
-- ('Giorgia.M@prova.prova', 'Giorgia', 'M', '1985-02-02', 'password2', true, false, '2024-07-02 11:00:00', '2024-07-11 11:00:00', '2024-07-02 11:00:00', '2024-12-31 23:59:59'),
-- ('Giogia.Q@prova.prova', 'Giorgia', 'Q', '1978-03-03', 'password3', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- -- Insegnanti di matematica e fisica superiori
-- ('Marco.C@prova.prova', 'Marco', 'C', '1978-03-03', 'password4', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Ilaria@prova.prova', 'Ilaria', 'Ilaria', '1978-03-03', 'password5', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Alberto@prova.prova', 'Alberto', 'Alberto', '1978-03-03', 'password6', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Riccardo@prova.prova', 'Riccardo', 'Q', '1978-03-03', 'password7', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Andrea@prova.prova', 'Andrea', 'Andrea', '1978-03-03', 'password8', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),

-- ---Psicologhe aiuto compiti elementari e medie per ragazzi certificati ---
-- ('Noemi@prova.prova', 'Noemi', 'Noemi', '1978-03-03', 'password9', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Giovanna@prova.prova', 'Giovanna', 'Giovanna', '1978-03-03', 'password10', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Irene@prova.prova', 'Irene', 'Irene', '1978-03-03', 'password11', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- -- ('Marco.C@prova.prova', 'Marco', 'C', '1978-03-03', 'password12', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),

-- --- altre materie ---
-- ('Aroon.Costantino@prova.prova', 'Aroon', 'Costantino', '1978-03-03', 'password13', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Elena@prova.prova', 'Elena', 'Elena', '1978-03-03', 'password14', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- ('Gaia@prova.prova', 'Gaia', 'Gaia', '1978-03-03', 'password15', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),

-- --- altre materie ---
-- ('Aurora@prova.prova', 'Aurora', 'Barban', '1978-03-03', 'password16', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),

-- --- psicologa di formazione per compiti elementari e medie per ragazzi certificati
-- ('Valeria@prova.prova', 'Valeria', 'Valeria', '1978-03-03', 'password17', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),

-- ('Marco.T@prova.prova', 'Marco', 'T', '1978-03-03', 'password18', true, false, '2024-07-03 12:00:00', '2024-07-12 12:00:00', '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- -- Utenti che sono studenti (student)
-- ('student1@prova.prova', 'Alice', 'Brown', '2005-04-04', 'password19', true, false, '2024-07-04 13:00:00', '2024-07-13 13:00:00', '2024-07-04 13:00:00', '2024-12-31 23:59:59'),
-- ('student2@prova.prova', 'Charlie', 'Davis', '2006-05-05', 'password20', true, false, '2024-07-05 14:00:00', '2024-07-14 14:00:00', '2024-07-05 14:00:00', '2024-12-31 23:59:59'),
-- ('student3@prova.prova', 'Emily', 'Evans', '2007-06-06', 'password21', true, false, '2024-07-06 15:00:00', '2024-07-15 15:00:00', '2024-07-06 15:00:00', '2024-12-31 23:59:59'),
-- ('student4@prova.prova', 'Frank', 'Garcia', '2008-07-07', 'password22', true, false, '2024-07-07 16:00:00', '2024-07-16 16:00:00', '2024-07-07 16:00:00', '2024-12-31 23:59:59'),
-- ('student5@prova.prova', 'Gigio', 'Donnaruma', '2008-07-07', 'password22', true, false, '2024-07-07 16:00:00', '2024-07-16 16:00:00', '2024-07-07 16:00:00', '2024-12-31 23:59:59'),
-- ('student6@prova.prova', 'Alessandro', 'Del Piero', '2008-07-07', 'password22', true, false, '2024-07-07 16:00:00', '2024-07-16 16:00:00', '2024-07-07 16:00:00', '2024-12-31 23:59:59'),
-- ('student7@prova.prova', 'Fabio', 'Cannavaro', '2008-07-07', 'password22', true, false, '2024-07-07 16:00:00', '2024-07-16 16:00:00', '2024-07-07 16:00:00', '2024-12-31 23:59:59'),
-- ('student8@prova.prova', 'Cristiano', 'Ronaldo', '2008-07-07', 'password22', true, false, '2024-07-07 16:00:00', '2024-07-16 16:00:00', '2024-07-07 16:00:00', '2024-12-31 23:59:59'),
-- ('student9@prova.prova', 'Gigi', 'D agostino', '2008-07-07', 'password22', true, false, '2024-07-07 16:00:00', '2024-07-16 16:00:00', '2024-07-07 16:00:00', '2024-12-31 23:59:59');

-- -- Inserimento dati nella tabella student
-- INSERT INTO public.student (id, id_school_grade, preliminary_meeting) VALUES 
-- (19, 1, true),  -- Alice Brown
-- (20, 2, false), -- Charlie Davis
-- (21, 3, true),  -- Emily Evans
-- (22, 2, false), -- Frank Garcia
-- (23, 1, true), -- Gigio Donnaruma
-- (24, 2, false), -- Alessandro Del Piero
-- (25, 3, false), -- Fabio Cannavaro
-- (26, 1, false), -- Cristiano Ronaldo
-- (27, 3, true); -- Gigi D agostino

-- -- Inserimento dati nella tabella teacher
-- INSERT INTO public.teacher (id) VALUES 
-- (2),  -- Federica M
-- (3),  -- Giorgia M
-- (4),  -- Giorgia Q
-- (5),  -- Marco C
-- (6),  -- Ilaria
-- (7),  -- Alberto
-- (8),  -- Riccardo
-- (9),  -- Andrea
-- (10),  -- Noemi
-- (11),  -- Giovanna
-- (12),  -- Irene
-- (13),  -- Aroon Costantino
-- (14),  -- Elena
-- (15),  -- Gaia
-- (16),  -- Aurora Barban
-- (17),  -- Valeria Valeria
-- (18);  -- Marco T


-- Inserimento dati nella tabella chief
INSERT INTO public.chief (id) VALUES 
(1); -- Martina Lucarda

-- Inserimento dati nella tabella teacher_school_subject
-- INSERT INTO public.teacher_school_subject (id, id_school_grade, id_subject) VALUES 
-- (2, 3, 1), -- Federica M insegna Inglese alle superiori
-- (2, 3, 2), -- Federica M insegna spagnolo alle superiori
-- (2, 1, 1), -- Federica M insegna Inglese alle elementari
-- (2, 1, 4), -- Federica M insegna Matematica alle elementari
-- (2, 1, 10), -- Federica M insegna Italiano alle elementari
-- (2, 1, 11), -- Federica M insegna Storia alle elementari
-- (2, 1, 12), -- Federica M insegna Geografia alle elementari
-- (2, 1, 13), -- Federica M insegna Geometria alle elementari
-- (2, 1, 14), -- Federica M insegna Scienze alle elementari
-- (2, 1, 15), -- Federica M insegna Arte e immagine alle elementari
-- (2, 2, 1), -- Federica M insegna Inglese alle medie
-- (2, 2, 2), -- Federica M insegna spagnolo alle medie
-- (2, 2, 4), -- Federica M insegna Matematica alle medie
-- (2, 2, 10), -- Federica M insegna Italiano alle medie
-- (2, 2, 11), -- Federica M insegna Storia alle medie
-- (2, 2, 12), -- Federica M insegna Geografia alle medie
-- (2, 2, 13), -- Federica M insegna Geometria alle medie
-- (2, 2, 14), -- Federica M insegna Scienze alle medie
-- (2, 2, 15), -- Federica M insegna Arte e immagine alle medie
-- (2, 2, 18), -- Federica M insegna tecnologia alle medie

-- (3, 3, 1),  -- Giorgia M insegna Inglese alle superiori
-- (3, 3, 2),  -- Giorgia M insegna spagnolo alle superiori
-- (3, 1, 1),  -- Giorgia M insegna Inglese alle elementari
-- (3, 1, 4),  -- Giorgia M insegna Matematica alle elementari
-- (3, 1, 10), -- Giorgia M insegna Italiano alle elementari
-- (3, 1, 11), -- Giorgia M insegna Storia alle elementari
-- (3, 1, 12), -- Giorgia M insegna Geografia alle elementari
-- (3, 1, 13), -- Giorgia M insegna Geometria alle elementari
-- (3, 1, 14), -- Giorgia M insegna Scienze alle elementari
-- (3, 1, 15), -- Giorgia M insegna Arte e immagine alle elementari
-- (3, 2, 1),  -- Giorgia M insegna Inglese alle medie
-- (3, 2, 2),  -- Giorgia M insegna spagnolo alle medie
-- (3, 2, 4),  -- Giorgia M insegna Matematica alle medie
-- (3, 2, 10), -- Giorgia M insegna Italiano alle medie
-- (3, 2, 11), -- Giorgia M insegna Storia alle medie
-- (3, 2, 12), -- Giorgia M insegna Geografia alle medie
-- (3, 2, 13), -- Giorgia M insegna Geometria alle medie
-- (3, 2, 14), -- Giorgia M insegna Scienze alle medie
-- (3, 2, 15), -- Giorgia M insegna Arte e immagine alle medie
-- (3, 2, 18), -- Giorgia M insegna tecnologia alle medie

-- (4, 3, 1),  -- Giorgia Q insegna Inglese alle superiori
-- (4, 3, 2),  -- Giorgia Q insegna spagnolo alle superiori
-- (4, 2, 1),  -- Giorgia Q insegna Inglese alle medie
-- (4, 2, 2),  -- Giorgia Q insegna spagnolo alle medie
-- (4, 2, 3),  -- Giorgia Q insegna tedesco alle medie
-- (4, 1, 1),  -- Giorgia Q insegna Inglese alle elementari

-- (5, 1, 1),  -- Marco C insegna Inglese alle elementari
-- (5, 1, 4),  -- Marco C insegna Matematica alle elementari
-- (5, 1, 10), -- Marco C insegna Italiano alle elementari
-- (5, 1, 11), -- Marco C insegna Storia alle elementari
-- (5, 1, 12), -- Marco C insegna Geografia alle elementari
-- (5, 1, 13), -- Marco C insegna Scienze alle elementari
-- (5, 1, 15), -- Marco C insegna Arte e immagine alle elementari
-- (5, 2, 1),  -- Marco C insegna Inglese alle medie
-- (5, 2, 4),  -- Marco C insegna Matematica alle medie
-- (5, 2, 10), -- Marco C insegna Italiano alle medie
-- (5, 2, 11), -- Marco C insegna Storia alle medie
-- (5, 2, 12), -- Marco C insegna Geografia alle medie
-- (5, 2, 13), -- Marco C insegna Scienze alle medie
-- (5, 2, 15), -- Marco C insegna Arte e immagine alle medie
-- (5, 2, 2),  -- Marco C insegna spagnolo alle medie
-- (5, 2, 3),  -- Marco C insegna tedesco alle medie
-- (5, 2, 17), -- Marco C insegna francese alle medie
-- (5, 2, 14), -- Marco C insegna Scienze alle medie
-- (5, 2, 18), -- Marco C insegna tecnologia alle medie
-- (5, 3, 4),  -- Marco C insegna matematica alle superiori

-- (6, 3, 4), -- Ilaria insegna matematica alle superiori (solo biennio)
-- (6, 3, 6), -- Ilaria insegna economia alle superiori

-- (7, 3, 4), -- Alberto insegna matematica alle superiori (triennio)
-- (7, 3, 5), -- Alberto insegna fisica alle superiori

-- (8, 3, 4), -- Riccardo insegna matematica alle superiori
-- (8, 3, 5), -- Riccardo insegna fisica alle superiori

-- (9, 3, 4), -- Andrea insegna matematica alle superiori
-- (9, 3, 5), -- Andrea insegna fisica alle superiori
-- (9, 3, 7), -- Andrea insegna chimica alle superiori

-- (10, 1, 1),  -- Noemi insegna Inglese alle elementari
-- (10, 1, 4),  -- Noemi insegna Matematica alle elementari
-- (10, 1, 10), -- Noemi insegna Italiano alle elementari
-- (10, 1, 11), -- Noemi insegna Storia alle elementari
-- (10, 1, 12), -- Noemi insegna Geografia alle elementari
-- (10, 1, 13), -- Noemi insegna Scienze alle elementari
-- (10, 1, 15), -- Noemi insegna Arte e immagine alle elementari
-- (10, 2, 1),  -- Noemi insegna Inglese alle medie
-- (10, 2, 4),  -- Noemi insegna Matematica alle medie
-- (10, 2, 10), -- Noemi insegna Italiano alle medie
-- (10, 2, 11), -- Noemi insegna Storia alle medie
-- (10, 2, 12), -- Noemi insegna Geografia alle medie
-- (10, 2, 13), -- Noemi insegna Scienze alle medie
-- (10, 2, 15), -- Noemi insegna Arte e immagine alle medie
-- (10, 2, 2),  -- Noemi insegna spagnolo alle medie
-- (10, 2, 3),  -- Noemi insegna tedesco alle medie
-- (10, 2, 17), -- Noemi insegna francese alle medie

-- (11, 1, 1),  -- Giovanna insegna Inglese alle elementari
-- (11, 1, 4),  -- Giovanna insegna Matematica alle elementari
-- (11, 1, 10), -- Giovanna insegna Italiano alle elementari
-- (11, 1, 11), -- Giovanna insegna Storia alle elementari
-- (11, 1, 12), -- Giovanna insegna Geografia alle elementari
-- (11, 1, 13), -- Giovanna insegna Scienze alle elementari
-- (11, 1, 15), -- Giovanna insegna Arte e immagine alle elementari
-- (11, 2, 1),  -- Giovanna insegna Inglese alle medie
-- (11, 2, 4),  -- Giovanna insegna Matematica alle medie
-- (11, 2, 10), -- Giovanna insegna Italiano alle medie
-- (11, 2, 11), -- Giovanna insegna Storia alle medie
-- (11, 2, 12), -- Giovanna insegna Geografia alle medie
-- (11, 2, 13), -- Giovanna insegna Scienze alle medie
-- (11, 2, 15), -- Giovanna insegna Arte e immagine alle medie
-- (11, 2, 2),  -- Giovanna insegna spagnolo alle medie
-- (11, 2, 3),  -- Giovanna insegna tedesco alle medie
-- (11, 2, 17), -- Giovanna insegna francese alle medie

-- (12, 1, 1),  -- Irene insegna Inglese alle elementari
-- (12, 1, 4),  -- Irene insegna Matematica alle elementari
-- (12, 1, 10), -- Irene insegna Italiano alle elementari
-- (12, 1, 11), -- Irene insegna Storia alle elementari
-- (12, 1, 12), -- Irene insegna Geografia alle elementari
-- (12, 1, 13), -- Irene insegna Scienze alle elementari
-- (12, 1, 15), -- Irene insegna Arte e immagine alle elementari
-- (12, 2, 1),  -- Irene insegna Inglese alle medie
-- (12, 2, 4),  -- Irene insegna Matematica alle medie
-- (12, 2, 10), -- Irene insegna Italiano alle medie
-- (12, 2, 11), -- Irene insegna Storia alle medie
-- (12, 2, 12), -- Irene insegna Geografia alle medie
-- (12, 2, 13), -- Irene insegna Scienze alle medie
-- (12, 2, 15), -- Irene insegna Arte e immagine alle medie
-- (12, 2, 2),  -- Irene insegna spagnolo alle medie
-- (12, 2, 3),  -- Irene insegna tedesco alle medie
-- (12, 2, 17), -- Irene insegna francese alle medie

-- (13, 3, 3),  -- Aroon insegna tedesco alle superiori
-- (13, 2, 3),  -- Aroon insegna tedesco alle medie
-- (13, 3, 8),  -- Aroon insegna diritto alle superiori
-- (13, 2, 1),  -- Aroon insegna Inglese alle medie
-- (13, 2, 4),  -- Aroon insegna Matematica alle medie
-- (13, 2, 10), -- Aroon insegna Italiano alle medie
-- (13, 2, 11), -- Aroon insegna Storia alle medie
-- (13, 2, 12), -- Aroon insegna Geografia alle medie
-- (13, 2, 13), -- Aroon insegna Geometria alle medie
-- (13, 2, 14), -- Aroon insegna Scienze alle medie
-- (13, 2, 15), -- Aroon insegna Arte e immagine alle medie
-- (13, 2, 18), -- Aroon insegna tecnologia alle medie


-- (14, 2, 1),  -- Elena insegna Inglese alle medie
-- (14, 2, 4),  -- Elena insegna Matematica alle medie
-- (14, 2, 10), -- Elena insegna Italiano alle medie
-- (14, 2, 11), -- Elena insegna Storia alle medie
-- (14, 2, 12), -- Elena insegna Geografia alle medie
-- (14, 2, 13), -- Elena insegna Geometria alle medie
-- (14, 2, 14), -- Elena insegna Scienze alle medie
-- (14, 2, 15), -- Elena insegna Arte e immagine alle medie
-- (14, 2, 18), -- Elena insegna tecnologia alle medie
-- (14, 2, 2),  -- Elena insegna spagnolo alle medie

-- (15, 1, 1),  -- Gaia insegna Inglese alle elementari
-- (15, 1, 4),  -- Gaia insegna Matematica alle elementari
-- (15, 1, 10), -- Gaia insegna Italiano alle elementari
-- (15, 1, 11), -- Gaia insegna Storia alle elementari
-- (15, 1, 12), -- Gaia insegna Geografia alle elementari
-- (15, 1, 13), -- Gaia insegna Scienze alle elementari
-- (15, 1, 15), -- Gaia insegna Arte e immagine alle elementari
-- (15, 2, 1),  -- Gaia insegna Inglese alle medie
-- (15, 2, 4),  -- Gaia insegna Matematica alle medie
-- (15, 2, 10), -- Gaia insegna Italiano alle medie
-- (15, 2, 11), -- Gaia insegna Storia alle medie
-- (15, 2, 12), -- Gaia insegna Geografia alle medie
-- (15, 2, 13), -- Gaia insegna Scienze alle medie
-- (15, 2, 15), -- Gaia insegna Arte e immagine alle medie
-- (15, 2, 2),  -- Gaia insegna spagnolo alle medie
-- (15, 2, 3),  -- Gaia insegna tedesco alle medie
-- (15, 2, 17), -- Gaia insegna francese alle medie

-- (16, 1, 1),  -- Aurora insegna Inglese alle elementari
-- (16, 1, 4),  -- Aurora insegna Matematica alle elementari
-- (16, 1, 10), -- Aurora insegna Italiano alle elementari
-- (16, 1, 11), -- Aurora insegna Storia alle elementari
-- (16, 1, 12), -- Aurora insegna Geografia alle elementari
-- (16, 1, 13), -- Aurora insegna Scienze alle elementari
-- (16, 1, 15), -- Aurora insegna Arte e immagine alle elementari
-- (16, 2, 1),  -- Aurora insegna Inglese alle medie
-- (16, 2, 4),  -- Aurora insegna Matematica alle medie
-- (16, 2, 10), -- Aurora insegna Italiano alle medie
-- (16, 2, 11), -- Aurora insegna Storia alle medie
-- (16, 2, 12), -- Aurora insegna Geografia alle medie
-- (16, 2, 13), -- Aurora insegna Scienze alle medie
-- (16, 2, 15), -- Aurora insegna Arte e immagine alle medie
-- (16, 2, 14), -- Aurora insegna Scienze alle medie
-- (16, 2, 18), -- Aurora insegna tecnologia alle medie
-- (16, 3, 6),  -- Aurora insegna economia alle superiori

-- (17, 1, 1),  -- Valeria insegna Inglese alle elementari
-- (17, 1, 4),  -- Valeria insegna Matematica alle elementari
-- (17, 1, 10), -- Valeria insegna Italiano alle elementari
-- (17, 1, 11), -- Valeria insegna Storia alle elementari
-- (17, 1, 12), -- Valeria insegna Geografia alle elementari
-- (17, 1, 13), -- Valeria insegna Geometria alle elementari
-- (17, 1, 14), -- Valeria insegna Scienze alle elementari
-- (17, 1, 15), -- Valeria insegna Arte e immagine alle elementari
-- (17, 2, 1),  -- Valeria insegna Inglese alle medie
-- (17, 2, 2),  -- Valeria insegna spagnolo alle medie
-- (17, 2, 4),  -- Valeria insegna Matematica alle medie
-- (17, 2, 10), -- Valeria insegna Italiano alle medie
-- (17, 2, 11), -- Valeria insegna Storia alle medie
-- (17, 2, 12), -- Valeria insegna Geografia alle medie
-- (17, 2, 13), -- Valeria insegna Geometria alle medie
-- (17, 2, 14), -- Valeria insegna Scienze alle medie
-- (17, 2, 15), -- Valeria insegna Arte e immagine alle medie
-- (17, 2, 18), -- Valeria insegna tecnologia alle medie

-- (18, 3, 9); -- Marco T insegna latino alle superiori


-- Inserimento dati nella tabella anag_slot
INSERT INTO public.anag_slot (id_slot) VALUES 
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10),
(11),
(12),
(13),
(14),
(15),
(16),
(17),
(18),
(19),
(20);