FROM python:3.7-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy in your requirements file
COPY ./bse_data_collector/requirements.txt ./

RUN set -ex \
    && BUILD_DEPS=" \
        build-essential \
        libpcre3-dev \
        libpq-dev \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && apt-get install -y --no-install-recommends default-libmysqlclient-dev \
    && pip install -U pip \
    && pip install --no-cache-dir -r /requirements.txt 

# Copy your application code to the container (make sure you create a .dockerignore file if any large files or directories should be excluded)
RUN mkdir /bse_data_collector/
WORKDIR /bse_data_collector/
COPY ./bse_data_collector/ /bse_data_collector/


# uWSGI will listen on this port
EXPOSE 8000