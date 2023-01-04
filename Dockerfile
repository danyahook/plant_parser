FROM joyzoursky/python-chromedriver:3.9

WORKDIR /usr/src/plant_parser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p ./src/parsed_data

COPY requirements.txt /usr/src/plant_parser/requirements.txt

RUN pip install -U pip --no-cache-dir && \
    pip install --no-cache-dir wheel && \
    pip install --no-cache-dir -r requirements.txt

COPY entrypoint.sh /usr/src/plant_parser/entrypoint.sh

COPY ./src /usr/src/plant_parser/src

RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]