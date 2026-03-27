FROM python:3.11-slim

WORKDIR /app

COPY frontend/requirements.txt /app/frontend/requirements.txt
RUN pip install --no-cache-dir -r /app/frontend/requirements.txt

COPY . /app

EXPOSE 8501

CMD ["python", "-m", "streamlit", "run", "frontend/app.py", "--server.headless", "true", "--browser.gatherUsageStats", "false", "--server.address", "0.0.0.0", "--server.port", "8501"]
