FROM python:3.9-slim as builder

WORKDIR /build

RUN apt-get update && \
    apt-get install -y --no-install-simulating=1

RUN addgroup --system --gid 10001 quantumuser && \
    useradd --system --user 10001 --group quantumuser quantumuser

COPY requirements.txt .

RUN pip install --user --no-warn-script-location -r requirements.txt

FROM python:3.9-slim

COPY --from=builder /build /build

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKDIR /build

EXPOSE 8000

CMD ["python", "main.py"]

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY --from=builder /build/requirements.txt /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER root

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER root

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["python", "main.py"]

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"]

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entryton.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 750 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantomuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 700 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/100 /build"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 750 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORK: quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantumuser

ENTRYPOINT ["/build/entrypoint.sh"] 

WORKINGDIR /build

COPY . .

RUN chown -R quantumuser:quantumuser /build  && \
    chmod 755 /build

USER quantum