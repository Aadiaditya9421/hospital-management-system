FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV FLASK_APP=run.py
ENV PORT=5000

# Expose the port
EXPOSE $PORT

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
