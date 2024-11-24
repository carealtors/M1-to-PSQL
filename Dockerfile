FROM postgres:alpine

# Install Python for parsing the spreadsheet
RUN apk add --no-cache python3 py3-pip

# Set the working directory
WORKDIR /app

# Copy the Python script for parsing
COPY utils/parse_spreadsheet.py /app/
COPY utils/requirements.txt /app/

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# Run the Python script to parse the spreadsheet before initializing the database
RUN /app/venv/bin/python parse_spreadsheet.py

# Copy SQL files for initialization
COPY setup.sql /docker-entrypoint-initdb.d/
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Ensure files are readable
RUN chmod a+r /docker-entrypoint-initdb.d/*

# Expose the desired port
EXPOSE 7777
