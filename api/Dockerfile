FROM python:3.12.3-alpine3.19 as builder

RUN python -mvenv construction_pyenv && source /construction_pyenv/bin/activate
COPY . /build
WORKDIR /build
RUN apk update \
  && apk add g++ libffi-dev make \
  && source /construction_pyenv/bin/activate \
  && pip install poetry --no-cache-dir \
  && poetry env remove --all \
  && poetry install --no-cache --no-root

FROM python:3.12.3-alpine3.19

COPY --from=builder /construction_pyenv /construction_pyenv
COPY --from=builder /build/construction /app
ENV PATH="/construction_pyenv/bin:$PATH"
WORKDIR /app

CMD ["gunicorn", "-b0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "construction.wsgi:application"]
