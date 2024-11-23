FROM postgres:alpine

# Copy SQL files for initialization
COPY *.sql /docker-entrypoint-initdb.d/
COPY ./m1-data/ /tmp/m1-data 
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Ensure files are readable
RUN chmod a+r /docker-entrypoint-initdb.d/*

# Expose the desired port
EXPOSE 7777
