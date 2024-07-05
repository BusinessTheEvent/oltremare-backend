# oltremare-backend
Backend per Oltremare


# Quickstart

(Only once) python3 -m venv ./venv

(To activate environment on linux) source ./venv/bin/activate

(To activate environment on windows) .\venv\Scripts\activate

(To run app) execute run.sh

(To run database) `sudo docker run --name oltremareDB \
 -e POSTGRES_PASSWORD=oltremare-password \
 -e POSTGRES_USER=oltremare-user \
 -e POSTGRES_DB=oltremare-dev \
 -p 5432:5432 \
 postgres`