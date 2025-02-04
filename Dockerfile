FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000

CMD ["sh", "-c", "python app.py"]
