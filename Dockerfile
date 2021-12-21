FROM python:3.8

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Copying application to the container and setting working directory:
COPY velkozz_web_api /home/app/velkoz_web_api
WORKDIR /home/app/velkoz_web_api

# Running all of the python install components:
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Configuring and starting the Django Project via a bash script: 
CMD ["bash", "start_server.sh"]

