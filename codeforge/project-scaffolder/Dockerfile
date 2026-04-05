FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY setup.py .
COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim as runtime

ENV USER=dockeruser
ENV UID=10001
ENV GID=10001

RUN groupadd --gid $GID $USER && \
    useradd --uid $UID --gid $GID -m $USER

WORKDIR /app

COPY --from=builder /root/.local/lib/python3.11/site-packages /root/.local/lib/python3.11/site-packages
COPY --from=builder /app/requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/* && \
    chown -R $USER:$USER /app

COPY --from=builder /app/setup.py .
COPY --from=builder /app/src ./src

RUN pip install --no-cache-dir --user -e .

USER $USER

ENTRYPOINT ["python", "-m", "project_scaffolder"]