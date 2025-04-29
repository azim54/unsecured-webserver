FROM python:3.12-slim

# Create app directory
RUN mkdir -p /usr/src/webserver
WORKDIR /usr/src/webserver
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
#EXPOSE ${PORT}

CMD ["python", "src/server.py"]
