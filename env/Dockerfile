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

# Create user and group
RUN groupadd -g 3990 appgroup && useradd -u 3990 --gid appgroup -ms /bin/bash appuser
RUN mkdir $MAIN && chown -R appuser:appgroup $MAIN

USER appuser
# update environment variables
ENV PYTHONPATH=$MAIN
ENV PYTHONUSERBASE=/home/appuser/.local
ENV PATH=/home/appuser/.local/bin:$PATH
ENV TZ=Europe/Belgrade

COPY --from=builder --chown=appuser:appgroup /home/appuser/.local /home/appuser/.local
WORKDIR $MAIN
COPY --chown=appuser:appgroup *.py ./
RUN mkdir -p /home/appuser/telegate

CMD [ "python", "main.py" ]
