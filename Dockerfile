FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./src /app/src
COPY ./.env /app/.env
COPY ./credentials.json /app/credentials.json
COPY ./email_template.html /app/email_template.html


# Run app.py when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]