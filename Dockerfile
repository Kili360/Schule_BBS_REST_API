# Nutzen der schlanken Python-Version auf Alpine Linux
FROM python:3.11-alpine

# Arbeitsverzeichnis im Container festlegen
WORKDIR /app

# Requirements kopieren und installieren
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Den restlichen App-Code kopieren (inkl. der HTML-Templates)
COPY . .

# Den Port deiner App (1234) nach außen hin öffnen
EXPOSE 1234

# Befehl zum Starten der App
CMD ["python", "app.py"]
