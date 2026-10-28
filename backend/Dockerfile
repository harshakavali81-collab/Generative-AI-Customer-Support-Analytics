FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
COPY src ./src
COPY data/source_docs ./data/source_docs
RUN useradd --create-home app && mkdir -p /app/instance && chown app:app /app/instance
USER app
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --start-period=15s --retries=3 CMD python -c "from urllib.request import urlopen; urlopen('http://127.0.0.1:8000/api/health', timeout=2).read()" || exit 1
CMD ["uvicorn","backend.app.main:app","--host","0.0.0.0","--port","8000"]
