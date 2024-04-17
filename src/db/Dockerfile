# syntax=docker/dockerfile:1
FROM postgres:16.2-bookworm

# Set the working directory inside the container
WORKDIR /app/db

# Copy the SQL scripts to the working directory
COPY database.sql /docker-entrypoint-initdb.d/

# Command to run the SQL scripts
CMD ["postgres"]
