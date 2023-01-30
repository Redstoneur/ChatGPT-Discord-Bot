FROM python:3.8

# mettre l'heure à Paris
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# create and set working directory
WORKDIR /app

# copy files to working directory without .dockerignore files
COPY . .

# install dependencies
RUN pip install -r requirements.txt

# run the command to start app
CMD ["python", "setup.py"]



