FROM python:3.9-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY src/ src/
COPY src/models.py src/
COPY src/main.py src/skill_library_predictor/
COPY src/skill_library_predictor/ src/
COPY . .
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]