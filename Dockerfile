# syntax=docker/dockerfile:1
FROM python:3.12-slim

LABEL maintainer="NoCountry Architecture Team"
LABEL description="Acelerador de Integraciones Open Source y Consultoria B2B"

WORKDIR /app

ENV PORT=8080 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir -p /app/data

COPY backend /app/backend
COPY frontend /app/frontend

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python3 -c "import urllib.request; urllib.request.urlopen('http://localhost:' + str(__import__('os').getenv('PORT', 8080)) + '/api/stats')" || exit 1

CMD ["python3", "backend/app.py"]
