FROM python:3.9-slim AS builder

RUN adduser --disabled-password --gecos '' --home /app --force-badname appuser appuser

WORKDIR /app

COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.9-slim

COPY --from=builder /app/.local /app/.local
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /app/.local/lib/python* /app/.local/lib/python

COPY . .

EXPOSE 5000

CMD ["python", "src/main.py"]

HEALTHCHECK CMD curl --fail http://localhost:5000/health || exit 1