# oltremare-backend
Backend per Oltremare


## Quickstart

**(Only once Linux)** `python3 -m venv ./venv`

**(Only once Windows)** `python -m venv ./venv`

**(To activate environment on linux)** `source ./venv/bin/activate`

**(To activate environment on windows)** `.\venv\Scripts\activate`

**(To install requirements)** `pip install -r requirements.txt`

**(To run app)** execute run.sh

**(To run database)** `sudo docker run --rm --name oltremareDB -e POSTGRES_PASSWORD=oltremare-password -e POSTGRES_USER=oltremare-user -e POSTGRES_DB=oltremare-dev -p 5432:5432 postgres`
