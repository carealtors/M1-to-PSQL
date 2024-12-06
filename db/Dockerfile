# Use the official PostgreSQL image
FROM postgres:alpine

# Create the configuration directory for custom files
RUN mkdir -p /etc/postgresql/

# Copy a custom postgresql.conf file into the image
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

# Copy SQL files for database initialization (optional)
COPY ./setup.sql /docker-entrypoint-initdb.d/

# Set permissions for all initialization scripts
RUN chmod -R 755 /docker-entrypoint-initdb.d

# Set permissions for the custom configuration file
RUN chmod 644 /etc/postgresql/postgresql.conf

# Use the custom configuration file when starting PostgreSQL
CMD ["postgres", "-c", "config_file=/etc/postgresql/postgresql.conf"]

# Expose the default PostgreSQL port
EXPOSE 5432
