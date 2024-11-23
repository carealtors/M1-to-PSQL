# M1 Data Processing with PostgreSQL

This repository provides tools for importing and querying M1 data files into a PostgreSQL database using Docker.

## Prerequisites

1. Obtain the M1 data files from the official documentation or your organization's source. The required files include:
   - `808_DuesPaymentsExtract.m1`
   - `808_MemberExtract.m1`
   - `808_MemberSecondaryExtract.m1`
   - `808_OfficeExtract.m1`

2. Place the files in the `/m1-data` directory of your project structure or update the import paths in the provided SQL scripts.

## Setup

### Step 1: Configure the State Code
The state code `808` is currently hardcoded in file paths and SQL scripts. To use data for another state, rename the files and adjust the paths or replace `808` with the desired state code in the scripts.

### Step 2: Start the Docker Container
1. Ensure Docker and Docker Compose are installed on your system.
2. Clone this repository and navigate to its directory.
3. Start the container using the following command:
   ```console
   docker-compose up --build
    ```

This will:
Build and start a PostgreSQL container.
Import the M1 data files into the database.
Apply indexes for optimized queries.

### Step 3: Connect to the Database
Use psql or your preferred database client to connect to the database:
   ```console
   psql -h 127.0.0.1 -p 5432 -U myusername -d mydatabase
   ```

Replace myusername and mydatabase with the credentials configured in the docker-compose.yml file.

Querying the Data
Here are some useful queries to get started:

1. Get Dues Payments for a Member
Retrieve dues payments for a specific MEMBER_ID:

2. Join Payments with Member Information
Get member details along with their dues payments:


Troubleshooting
Frequent Checkpoints Warning
If you see warnings about frequent checkpoints in the logs, adjust the max_wal_size and other parameters in the postgresql.conf file.

Connection Issues
Ensure that PostgreSQL is listening on all interfaces (listen_addresses = '*') and that the docker-compose.yml file maps the correct ports.

License
This project is intended for internal use and complies with your organization's data handling policies. Ensure appropriate permissions before sharing or modifying the data.