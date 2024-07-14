-- Inserimento dati nella tabella groups
INSERT INTO public.groups (name, scopes) VALUES 
('Group 1', 'Scope 1'),
('Group 2', 'Scope 2'),
('Group 3', 'Scope 3'),
('Group 4', 'Scope 4');

-- Inserimento dati nella tabella roles
INSERT INTO public.roles (name, scopes) VALUES 
('Role 1', 'Scope 1'),
('Role 2', 'Scope 2'),
('Role 3', 'Scope 3'),
('Role 4', 'Scope 4');

-- Inserimento dati nella tabella school_grade
INSERT INTO public.school_grade (grade, price) VALUES 
('Elementari', 15.00),
('Medie', 18.00),
('Superiori', 22.00);

-- Inserimento dati nella tabella subjects
INSERT INTO public.subjects (name) VALUES 
('Math'),
('Science'),
('History'),
('Geography'),
('Literature'),
('Physics'),
('Chemistry'),
('Biology'),
('Art'),
('Music'),
('Physical Education'),
('Computer Science'),
('Economics'),
('Philosophy'),
('Sociology'),
('Psychology'),
('Political Science'),
('Environmental Science'),
('Foreign Languages'),
('Drama'),
('Engineering'),
('Business Studies'),
('Statistics'),
('Ethics'),
('Astronomy');

-- Inserimento dati nella tabella users
INSERT INTO public.users (username, name, surname, birthdate, password, is_active, disabled, additional_scopes, role_id, registered_at, last_login, is_application, date_init_validity, date_end_validity) 
VALUES 
-- Utenti che sono insegnanti (teacher)
('teacher1', 'John', 'Doe', '1990-01-01', 'password1', true, false, 'scope1', 1, '2024-07-01 10:00:00', '2024-07-10 10:00:00', false, '2024-07-01 10:00:00', '2024-12-31 23:59:59'),
('teacher2', 'Jane', 'Smith', '1985-02-02', 'password2', true, false, 'scope2', 2, '2024-07-02 11:00:00', '2024-07-11 11:00:00', false, '2024-07-02 11:00:00', '2024-12-31 23:59:59'),
('teacher3', 'Robert', 'Johnson', '1978-03-03', 'password3', true, false, 'scope3', 3, '2024-07-03 12:00:00', '2024-07-12 12:00:00', false, '2024-07-03 12:00:00', '2024-12-31 23:59:59'),
-- Utenti che sono studenti (student)
('student1', 'Alice', 'Brown', '2005-04-04', 'password4', true, false, 'scope4', 4, '2024-07-04 13:00:00', '2024-07-13 13:00:00', false, '2024-07-04 13:00:00', '2024-12-31 23:59:59'),
('student2', 'Charlie', 'Davis', '2006-05-05', 'password5', true, false, 'scope4', 4, '2024-07-05 14:00:00', '2024-07-14 14:00:00', false, '2024-07-05 14:00:00', '2024-12-31 23:59:59'),
('student3', 'Emily', 'Evans', '2007-06-06', 'password6', true, false, 'scope4', 4, '2024-07-06 15:00:00', '2024-07-15 15:00:00', false, '2024-07-06 15:00:00', '2024-12-31 23:59:59'),
('student4', 'Frank', 'Garcia', '2008-07-07', 'password7', true, false, 'scope4', 4, '2024-07-07 16:00:00', '2024-07-16 16:00:00', false, '2024-07-07 16:00:00', '2024-12-31 23:59:59'),
-- Utente che è chief
('chief1', 'George', 'Miller', '1970-08-08', 'password8', true, false, 'scope4', 4, '2024-07-08 17:00:00', '2024-07-18 17:00:00', false, '2024-07-08 17:00:00', '2024-12-31 23:59:59');

-- Inserimento dati nella tabella student
INSERT INTO public.student (id, id_school_grade, preliminary_meeting) VALUES 
(4, 1, true),  -- Alice Brown
(5, 2, false), -- Charlie Davis
(6, 3, true),  -- Emily Evans
(7, 3, false); -- Frank Garcia

-- Inserimento dati nella tabella teacher
INSERT INTO public.teacher (id) VALUES 
(1),  -- John Doe
(2),  -- Jane Smith
(3);  -- Robert Johnson

-- Inserimento dati nella tabella chief
INSERT INTO public.chief (id) VALUES 
(8); -- George Miller

-- Inserimento dati nella tabella teacher_school_subject
INSERT INTO public.teacher_school_subject (id, id_school_grade, id_subject) VALUES 
(1, 1, 1), -- John Doe teaching Math to Elementari
(2, 2, 2), -- Jane Smith teaching Science to Medie
(3, 3, 3); -- Robert Johnson teaching History to Superiori

-- Inserimento dati nella tabella user_group
INSERT INTO public.user_group (user_id, group_id) VALUES 
(1, 1), -- John Doe in Group 1
(2, 2), -- Jane Smith in Group 2
(3, 3), -- Robert Johnson in Group 3
(4, 4), -- Alice Brown in Group 4
(5, 1), -- Charlie Davis in Group 1
(6, 2), -- Emily Evans in Group 2
(7, 3), -- Frank Garcia in Group 3
(8, 4); -- George Miller in Group 4

-- Inserimento dati nella tabella booking
INSERT INTO public.booking (id_student, id_teacher, id_school_grade, id_subject, start_datetime, end_datetime, duration, notes, attended, insert_id_user, insert_date, insert_time)
VALUES 
(4, 1, 1, 1, '2023-01-01 09:00:00+00', '2023-01-01 10:00:00+00', 60, 'First meeting', true, 1, '2023-01-01', '09:00:00'),
(5, 1, 1, 2, '2023-01-02 11:00:00+00', '2023-01-02 12:00:00+00', 60, 'Second meeting', false, 1, '2023-01-02', '11:00:00'),
(6, 2, 2, 3, '2023-02-01 14:00:00+00', '2023-02-01 15:00:00+00', 60, 'Third meeting', true, 2, '2023-02-01', '14:00:00'),
(7, 3, 3, 4, '2023-02-02 16:00:00+00', '2023-02-02 17:00:00+00', 60, 'Fourth meeting', false, 3, '2023-02-02', '16:00:00');
