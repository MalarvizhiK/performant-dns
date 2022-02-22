FROM python:3

COPY . /application
WORKDIR /application
RUN mkdir -p /application/work  \
    && python3 -m pip install -r ./requirements.txt
ENV PYTHONPATH=/application
EXPOSE 8080

ENTRYPOINT [ "python3", "app/start.py" ]

