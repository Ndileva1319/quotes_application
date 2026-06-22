FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/
COPY app.py /app/
COPY templates/ /app/templates/
COPY quotes.html /app/

RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y vim

EXPOSE 5000
EXPOSE 443

CMD ["python", "app.py"]
