# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# environment variables for the app to run
ENV SPOTIPY_CLIENT_ID="9aa01b97021549f29427a140483c7759"
ENV SPOTIPY_CLIENT_SECRET="36b5fd231e5249ad9d4a4205451d87ce"
ENV SPOTIPY_REDIRECT_URI="http://127.0.0.1:8080"

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR ./src

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:app