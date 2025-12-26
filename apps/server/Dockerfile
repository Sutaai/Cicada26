FROM python:3.13-alpine

WORKDIR /app

COPY LICENSE README.md pyproject.toml pdm.lock ./

RUN pip install .

COPY cicada26/ ./cicada26

VOLUME [ "/wiki" ]
ENV C26_WIKI_PATH="/wiki"

CMD ["fastapi", "run", "/app/cicada26"]
