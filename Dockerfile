# Image of python with Debian
FROM python:3.10-bullseye

# Set Workdir
WORKDIR /home/app

# Envs for don't generate pycache
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Some important libs
RUN apt update && apt upgrade -y \
    && apt install gcc python3-dev musl-dev bash build-essential libssl-dev libffi-dev -y

# Upgrade pip, copy requirements and install all the project dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Entrypoint gonna be useful when we up the container
COPY entrypoint.sh .
RUN cat /home/app/entrypoint.sh
RUN sed -i 's/\r$//g' /home/app/entrypoint.sh
RUN chmod +x /home/app/entrypoint.sh

# Copy all the files for the root dir
COPY . .

ENTRYPOINT ["/home/app/entrypoint.sh"]
