CREATE TABLE IF NOT EXISTS users (
    "id" INTEGER PRIMARY KEY ,
    "username" VARCHAR UNIQUE,
    "name" VARCHAR,
    "surname" VARCHAR,
    "birthdate" TIMESTAMP,
    "password" VARCHAR,
    "is_active" BOOLEAN DEFAULT TRUE,
    "disabled" BOOLEAN DEFAULT FALSE,
    "registered_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "last_login" TIMESTAMP,
    "date_init_validity" TIMESTAMP,
    "date_end_validity" TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "school_grade" (
	"id_school_grade" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"grade" text NOT NULL,
	"price" numeric(8,2) NOT NULL,
	PRIMARY KEY ("id_school_grade")
);

CREATE TABLE IF NOT EXISTS "student" (
	"id" bigint NOT NULL,
	"id_school_grade" bigint NOT NULL,
	"preliminary_meeting" boolean NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "teacher" (
	"id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "subjects" (
	"id_subject" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"name" text NOT NULL,
	PRIMARY KEY ("id_subject")
); 

CREATE TABLE IF NOT EXISTS "booking" (
	"id_booking" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"id_student" bigint NOT NULL,
	"id_teacher" bigint NOT NULL,
	"id_school_grade" bigint NOT NULL,
	"id_subject" bigint NOT NULL,
	"start_datetime" timestamp with time zone NOT NULL,
	"end_datetime" timestamp with time zone NOT NULL,
	"duration" bigint NOT NULL,
	"notes" text,
	"attended"	boolean NOT NULL,
	"insert_id_user" bigint NOT NULL,
	"insert_date" date NOT NULL,
	"insert_time" time without time zone NOT NULL,
	PRIMARY KEY ("id_booking")
);

CREATE TABLE IF NOT EXISTS "teacher_school_subject" (
	"id" bigint NOT NULL,
	"id_school_grade" bigint NOT NULL,
	"id_subject" bigint NOT NULL,
	PRIMARY KEY ("id", "id_school_grade", "id_subject")
);

CREATE TABLE IF NOT EXISTS "chief" (
	"id" bigint NOT NULL,
	PRIMARY KEY ("id")
);

CREATE TABLE IF NOT EXISTS "anag_slot" (
	"id_slot" int NOT NULL, 
	PRIMARY KEY ("id_slot")
);

CREATE TABLE IF NOT EXISTS "booking_slot" (
	"id_booking" int NOT NULL, 
	"id_slot"    int NOT NULL,
	PRIMARY KEY ("id_booking", "id_slot")
);


CREATE TABLE IF NOT EXISTS "messages" (
	"id_message" bigint GENERATED ALWAYS AS IDENTITY NOT NULL UNIQUE,
	"id_sender" bigint NOT NULL,
	"id_receiver" bigint NOT NULL,
	"text" text NOT NULL,
	"send_datetime" timestamp with time zone NOT NULL,
	"is_read" boolean NOT NULL,
	PRIMARY KEY ("id_message")
);

ALTER TABLE "messages" ADD CONSTRAINT "messages_fk1" FOREIGN KEY ("id_sender") REFERENCES "users"("id");
ALTER TABLE "messages" ADD CONSTRAINT "messages_fk2" FOREIGN KEY ("id_receiver") REFERENCES "users"("id");

ALTER TABLE "student" ADD CONSTRAINT "student_fk0" FOREIGN KEY ("id") REFERENCES "users"("id");
ALTER TABLE "student" ADD CONSTRAINT "student_fk1" FOREIGN KEY ("id_school_grade") REFERENCES "school_grade"("id_school_grade");

ALTER TABLE "teacher" ADD CONSTRAINT "teacher_fk0" FOREIGN KEY ("id") REFERENCES "users"("id");

ALTER TABLE "booking" ADD CONSTRAINT "booking_fk1" FOREIGN KEY ("id_student") REFERENCES "student"("id");
ALTER TABLE "booking" ADD CONSTRAINT "booking_fk2" FOREIGN KEY ("id_teacher") REFERENCES "teacher"("id");
ALTER TABLE "booking" ADD CONSTRAINT "booking_fk3" FOREIGN KEY ("id_school_grade") REFERENCES "school_grade"("id_school_grade");
ALTER TABLE "booking" ADD CONSTRAINT "booking_fk4" FOREIGN KEY ("id_subject") REFERENCES "subjects"("id_subject");

ALTER TABLE "teacher_school_subject" ADD CONSTRAINT "teacher_school_subject_fk0" FOREIGN KEY ("id") REFERENCES "teacher"("id");
ALTER TABLE "teacher_school_subject" ADD CONSTRAINT "teacher_school_subject_fk1" FOREIGN KEY ("id_school_grade") REFERENCES "school_grade"("id_school_grade");
ALTER TABLE "teacher_school_subject" ADD CONSTRAINT "teacher_school_subject_fk2" FOREIGN KEY ("id_subject") REFERENCES "subjects"("id_subject");

ALTER TABLE "chief" ADD CONSTRAINT "chief_fk0" FOREIGN KEY ("id") REFERENCES "users"("id");