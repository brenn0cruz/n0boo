FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 LAB_DB=/data/lab.sqlite
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY engine.py storage.py app.py dashboard.html generate_demo.py seed.py ./
RUN useradd --create-home --uid 10001 lab && mkdir /data && chown lab:lab /data
USER lab
EXPOSE 8080
CMD ["sh", "-c", "python seed.py && exec uvicorn app:app --host 0.0.0.0 --port 8080"]
