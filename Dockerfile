FROM python:3

COPY app /app
WORKDIR /app
RUN mkdir -p /app/work  \
    && python3 -m pip install -r ./requirements.txt
ENV PYTHONPATH=/app
EXPOSE 5000

ENTRYPOINT [ "python3", "app/start.py" ]
