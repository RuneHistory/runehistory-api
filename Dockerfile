FROM alpine

LABEL maintainer="Jim Wright <jmwri93@gmail.com>"
LABEL description="RuneHistory API"

# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
    openssl-dev \
    libffi-dev \
    musl-dev \
    gcc \
    python3 \
    python3-dev \
    bash \
    nginx \
    uwsgi \
    uwsgi-python3 \
    supervisor && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    sed -i '/-e git+git@github.com/d' /tmp/requirements.txt && \
    pip3 install -r /tmp/requirements.txt && \
    rm /etc/nginx/conf.d/default.conf && \
    rm -r /root/.cache

COPY docker/nginx.conf /etc/nginx/
COPY docker/flask-site-nginx.conf /etc/nginx/conf.d/
COPY docker/uwsgi.ini /etc/uwsgi/
COPY docker/supervisord.conf /etc/supervisord.conf

COPY . /app
WORKDIR /app

ENTRYPOINT ["/usr/bin/supervisord"]
CMD ["-c", "/etc/supervisord.conf"]