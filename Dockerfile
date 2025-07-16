FROM python:3.12 as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

EXPOSE 8000

WORKDIR /app/src/agents/

CMD ["adk", "api_server", "--host", "0.0.0.0", "--port", "8000"]
