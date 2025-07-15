FROM python:3.12 as base

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ /app/src/


FROM base as agent

EXPOSE 8000

CMD ["sh", "-c", "cd src/agents && adk api_server --host 0.0.0.0 --port 8000"]


FROM base as app

EXPOSE 8501

CMD ["sh", "-c", "streamlit run src/app/main.py --server.address=0.0.0.0"]
