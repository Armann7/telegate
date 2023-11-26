# first stage
FROM python:3.11-slim AS builder

RUN useradd -ms /bin/bash appuser
USER appuser

# install dependencies to the local user directory
ENV PATH=/home/appuser/.local:/home/appuser/.local/bin:$PATH
COPY requirements.txt .
RUN python -m pip install --upgrade pip --disable-pip-version-check
RUN pip install --user -r requirements.txt

# second stage
FROM python:3.11-slim
LABEL maintainer="vyacheslav.v.kuzmin@gmail.com"
ENV MAIN=/app
ENV TELEGATE_DATA=/data

# Create user and group
RUN groupadd appgroup && useradd --gid appgroup -ms /bin/bash appuser
RUN mkdir $MAIN && chown -R appuser:appgroup $MAIN && mkdir $TELEGATE_DATA && chown -R appuser:appgroup $TELEGATE_DATA

USER appuser
# update environment variables
ENV PYTHONPATH=$MAIN
ENV PYTHONUSERBASE=/home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH
ENV TZ=Europe/Belgrade

COPY --from=builder --chown=appuser:appgroup /home/appuser/.local /home/appuser/.local
WORKDIR $MAIN
COPY --chown=appuser:appgroup src/* ./

ENTRYPOINT [ "python", "main.py" ]
