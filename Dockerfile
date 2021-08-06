# syntax=docker/dockerfile:experimental
FROM python:3.7

RUN apt-get update && apt-get install -y \
        build-essential  \
        vim

WORKDIR /app

# Pre-install requirements.txt
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Install application including those in Aquabyte PyPI
RUN mkdir -p -m 0600 ~/.ssh && ssh-keyscan github.com >> ~/.ssh/known_hosts
ENV PIP_EXTRA_INDEX_URL=http://aquabyte-repository.s3-website-us-west-1.amazonaws.com/pypi/
ENV PIP_TRUSTED_HOST=aquabyte-repository.s3-website-us-west-1.amazonaws.com

COPY dist/helloworld-app-latest.tar.gz /app
RUN --mount=type=ssh pip3 -v install --no-cache-dir helloworld-app-latest.tar.gz

#Prevents python logging from buffer to have lower latency for log messages in cloudwatch
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "4", "-t", "120", "helloworld_app.wsgi:app"]
