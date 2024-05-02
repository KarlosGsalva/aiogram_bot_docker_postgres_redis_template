# Separate "build" image
# Build stage
FROM python:3.12.3-slim-bullseye as compile-image

# create venv in /opt/venv directory
RUN python -m venv /opt/venv

# adds the path to the virtual environment executables to the PATH environment variable
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# --no-cache-dir don't save cached files
# bpython improved python shell
RUN pip install --no-cache-dir --upgrade pip \
&&  pip install bpython \
 && pip install --no-cache-dir -r requirements.txt

# "Run" image
# Run stage
FROM python:3.12.3-slim-bullseye

# copying venv from build stage
COPY --from=compile-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"


WORKDIR /app
COPY aiogram_bot_template /app
CMD ["python", "-m", "bot"]
