# Use the official PostgreSQL image
FROM postgres:alpine


# Create the configuration directory
RUN mkdir -p /etc/postgresql/

# Copy a custom postgresql.conf file (optional)
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Copy SQL files for database initialization
COPY ./setup.sql /docker-entrypoint-initdb.d/

# Ensure permissions are set correctly for the initialization scripts
RUN chmod -R 755 /docker-entrypoint-initdb.d

# Use the custom configuration file when starting PostgreSQL
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

# Expose the default PostgreSQL port
EXPOSE 5432
