# Use the official PostgreSQL image
FROM postgres:alpine

# Set environment variables for PostgreSQL from .env file
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB

# Create the configuration directory
RUN mkdir -p /etc/postgresql/

# Copy the custom postgresql.conf into the container
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Copy setup.sql into the initialization folder
COPY ./setup.sql /docker-entrypoint-initdb.d/

# Ensure the permissions are correct for the configuration file
RUN chmod 644 /etc/postgresql/postgresql.conf
RUN chmod 644 /docker-entrypoint-initdb.d/setup.sql

# Use the custom configuration file when starting PostgreSQL
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

# Expose the PostgreSQL port
EXPOSE 5432
