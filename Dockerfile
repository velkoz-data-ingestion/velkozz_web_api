#########################################################
# Dockerfile that builds and initalize the Velkozz Django
# Server.
#########################################################
FROM python:3.8

# Creating a user to switch to for security, not using root:
#RUN useradd -r -u 1111 django_server && usermod -aG sudo django_server

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Copying application to the container and setting working directory:
COPY velkozz_web_api /home/app/velkoz_web_api
WORKDIR /home/app/velkoz_web_api

# Running all of the python install components:
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Configuring and starting the Django Project via a bash script: 
ENTRYPOINT ["sh", "start_server.sh"]