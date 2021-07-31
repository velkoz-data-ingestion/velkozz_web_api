FROM python

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# Copying application to the container and setting working directory:
COPY velkozz_web_api /home/app/velkoz_web_api
WORKDIR /home/app/velkoz_web_api

# Running all of the python install components:
RUN pip install --no-cache-dir -r requirements.txt

RUN python manage.py collectstatic --noinput && python manage.py makemigrations && python manage.py migrate

CMD ["python", "manage.py", "migrate", "0.0.0.0:8000"]  
EXPOSE 8000
