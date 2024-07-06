# oltremare-backend
Backend per Oltremare


## Quickstart

**(Only once Linux)** `python3 -m venv ./venv`

**(Only once Windows)** `python -m venv ./venv`

**(To activate environment on linux)** `source ./venv/bin/activate`

**(To activate environment on windows)** `.\venv\Scripts\activate`

**(To install requirements)** `pip install -r requirements.txt`

**(To run app)** execute run.sh

**(To run database)** `sudo docker run --name oltremareDB -e POSTGRES_PASSWORD=oltremare-password -e POSTGRES_USER=oltremare-user -e POSTGRES_DB=oltremare-dev -p 5432:5432 postgres`


## DB schema

```mermaid

classDiagram
direction BT
class booking {
   bigint id_student
   bigint id_teacher
   date start_datetime
   date end_datetime
   bigint duration
   bigint subject
   text notes
   bigint id
}
class groups {
   varchar name
   varchar scopes
   integer id
}
class roles {
   varchar name
   varchar scopes
   integer id
}
class school_grade {
   text grade
   double precision price
   bigint id
}
class student {
   bigint id_user
   bigint school_grade
   boolean preliminary_meeting
   bigint id
}
class subjects {
   bigint name
   bigint id
}
class teacher {
   bigint user_id
   bigint schools
   bigint subjects
   bigint id
}
class teacher_school {
   bigint id_teacher
   bigint id_school
}
class teacher_subject {
   bigint id_teacher
   bigint id_subject
}
class user_group {
   integer user_id
   integer group_id
}
class users {
   varchar username
   varchar name
   varchar password
   boolean is_active
   boolean disabled
   varchar additional_scopes
   integer role_id
   timestamp registered_at
   timestamp last_login
   boolean is_application
   timestamp date_init_validity
   timestamp date_end_validity
   integer id
}

booking  -->  student : id_student:id;
booking  -->  teacher : id_teacher:id;
student  -->  school_grade : school_grade:id;
student  -->  users : id_user:id;
teacher  -->  users : user_id:id;
teacher_school  -->  school_grade : id_school:id;
teacher_school  -->  teacher : id_teacher:id;
teacher_subject  -->  subjects : id_subject:id;
teacher_subject  -->  teacher : id_teacher:id;
user_group  -->  groups : group_id:id;
user_group  -->  users : user_id:id;
users  -->  roles : role_id:id;
```
