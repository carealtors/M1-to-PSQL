# M1 and ACH Data Processing with PostgreSQL

This repository provides tools for importing and querying M1 data files and optionally processing NAR ACH files into a PostgreSQL database using Docker. There is also a flask api to expose the data.

## Prerequisites

1. Obtain the M1 data files from the [official documentation](https://nationalasnofrealtors.mcoutput.com/1374755/Content/Introduction/Welcome%20to%20M1.htm). The required files include:
   - `****_DuesPaymentsExtract.m1`
   - `****_MemberExtract.m1`
   - `****_MemberSecondaryExtract.m1`
   - `****_OfficeExtract.m1`

2. Place the files in the `/m1-data` directory of your project structure or update the import paths in the provided SQL scripts.

## NAR ACH Data Files (Optional)

If processing NAR ACH files is desired, place the ACH export files in the /ach-data directory. Ensure the toggle for ACH file processing is enabled in the .env file (see Setup below for details). ACH file processing is disabled by default.

## Setup

### Step 1: Configure the Association Code
The state code `808` is currently hardcoded in file paths and SQL scripts. To use data for another association, rename the files and adjust the paths or replace `808` with the desired association code in the scripts.

### Step 2: Start the Docker Container
1. Ensure Docker and Docker Compose are installed on your system.
2. Clone this repository and navigate to its directory.
3. Start the container using the following command:
   ```console
   docker-compose up --build
    ```

This will:
- Build and start a PostgreSQL container.
- Import the M1 data files into the database.
- Apply indexes for optimized queries.

### Step 3: Connect to the Database
Use psql or your preferred database client to connect to the database:
   ```console
   PGPASSWORD=mypassword psql -h 127.0.0.1 -p 7777 -U myusername -d mydatabase
   ```

Replace myusername, mypassword, port, and mydatabase with the credentials configured in the docker-compose.yml file.

### Step 4: Querying the Data
Here are some useful queries to get started:

1. Get Dues Payments for a Member
Retrieve dues payments for a specific MEMBER_ID:
``` sql
SELECT * 
FROM DuesPayments 
WHERE MEMBER_ID = 205578875;

```
2. Join Payments with Member Information
Get member and office details along with their dues payments:
``` sql
SELECT 
    dp.MEMBER_ID, 
    dp.PAYMENT_AMOUNT, 
    dp.BILLING_YEAR, 
    dp.PAYMENT_TYPE_CODE, 
    dp.DUES_PAID_DATE, 
    me.FIRST_NAME, 
    me.LAST_NAME, 
    me.PRIMARY_LOCAL_ASSOCIATION_ID AS LOCAL_ASSOCIATION, 
    oe.OFFICE_BUSINESS_NAME AS OFFICE_NAME
FROM 
    DuesPayments dp
LEFT JOIN 
    MemberExtract me ON dp.MEMBER_ID = me.MEMBER_ID
LEFT JOIN 
    OfficeExtract oe ON dp.OFFICE_ID = oe.OFFICE_ID
WHERE 
    dp.MEMBER_ID = 205578875;

```


3. Get Dues Payments by Local Association ID
``` sql
SELECT 
    dp.MEMBER_ID, 
    dp.PAYMENT_AMOUNT, 
    dp.BILLING_YEAR, 
    dp.DUES_PAID_DATE
FROM 
    DuesPayments dp
JOIN 
    MemberExtract me ON dp.MEMBER_ID = me.MEMBER_ID
WHERE 
    me.PRIMARY_LOCAL_ASSOCIATION_ID = 808;
```


4. Total Dues Paid by Association
``` sql
SELECT 
    me.PRIMARY_LOCAL_ASSOCIATION_ID, 
    SUM(dp.PAYMENT_AMOUNT) AS TOTAL_DUES
FROM 
    DuesPayments dp
JOIN 
    MemberExtract me ON dp.MEMBER_ID = me.MEMBER_ID
WHERE 
    me.PRIMARY_LOCAL_ASSOCIATION_ID = 808
GROUP BY 
    me.PRIMARY_LOCAL_ASSOCIATION_ID;
```

5. Total Count of Dues Payments in 2024 Missing EC_CONTROL_NUMBER with PAYMENT_TYPE_CODE = 'STAT'
``` sql
SELECT 
    COUNT(*) AS TOTAL_MISSING_EC_CONTROL
FROM 
    DuesPayments
WHERE 
    BILLING_YEAR = 2024
    AND EC_CONTROL_NUMBER IS NULL
    AND PAYMENT_TYPE_CODE = 'STAT';
```

6. Full Details of Payments Missing EC_CONTROL_NUMBER with PAYMENT_TYPE_CODE = 'STAT' and PRIMARY_STATE_ASSOCIATION_ID = '808'

``` sql 
SELECT 
    MEMBER_ID, 
    MEMBER_FIRST_NAME, 
    MEMBER_LAST_NAME, 
    INCURRING_MEMBER_ID, 
    INCURRING_MEMBER_FIRST_NAME, 
    INCURRING_MEMBER_LAST_NAME, 
    PRIMARY_ASSOCIATION_ID, 
    PRIMARY_STATE_ASSOCIATION_ID, 
    BILLING_ASSOCIATION_ID, 
    OFFICE_ID, 
    PAYMENT_TYPE_CODE, 
    BILLING_YEAR, 
    PAYMENT_AMOUNT, 
    CONTRIBUTION_TYPE_CODE, 
    DUES_PAID_DATE, 
    PAYMENT_SOURCE_CODE, 
    EC_CONTROL_NUMBER, 
    LAST_CHANGED_BY, 
    LAST_CHANGED_DATETIME
FROM 
    DuesPayments
WHERE 
    BILLING_YEAR = 2024
    AND EC_CONTROL_NUMBER IS NULL
    AND PAYMENT_TYPE_CODE = 'STAT'
    AND PRIMARY_STATE_ASSOCIATION_ID = '808';

```
7. Count of Dues Payments for 'STAT'  in 2024 without an EC Control Number
``` sql
SELECT 
    COUNT(*) AS TOTAL_MISSING_PRIMARY_STATE_AND_EC_CONTROL
FROM 
    DuesPayments
WHERE 
    PAYMENT_TYPE_CODE = 'STAT'
    AND EC_CONTROL_NUMBER IS NULL
    AND BILLING_YEAR = 2024;

```

8. Count of Dues Payments Types in 2024
```sql
SELECT 
    "PAYMENT_TYPE_CODE", 
    COUNT(*) AS "PaymentTypeCount"
FROM 
    "DuesPayments"
WHERE 
    "BILLING_YEAR" = 2024
GROUP BY 
    "PAYMENT_TYPE_CODE"
ORDER BY 
    "PaymentTypeCount" DESC;
```



## Troubleshooting
### Frequent Checkpoints Warning
If you see warnings about frequent checkpoints in the logs, adjust the max_wal_size and other parameters in the postgresql.conf file.

### Connection Issues
Ensure that PostgreSQL is listening on all interfaces (listen_addresses = '*') and that the docker-compose.yml file maps the correct ports.

##  License
This project is intended for internal use 


SELECT 
    "PAYMENT_TYPE_CODE", 
    COUNT(*) AS "PaymentTypeCount"
FROM 
    "DuesPayments"
WHERE 
    "BILLING_YEAR" = 2024
GROUP BY 
    "PAYMENT_TYPE_CODE"
ORDER BY 
    "PaymentTypeCount" DESC;

SELECT
    "DuesPayments"."BILLING_ASSOCIATION_ID",
    "AssociationDetails"."ASSOCIATION_NAME",
    COUNT(*) AS null_ec_control_number,
    COALESCE(total_payment_count.total_payments, 0) AS total_payments,
    ROUND(
        CASE 
            WHEN COALESCE(total_payment_count.total_payments, 0) > 0 THEN 
                ((COALESCE(total_payment_count.total_payments, 0) - COUNT(*))::NUMERIC 
                / COALESCE(total_payment_count.total_payments, 0)) * 100
            ELSE 0
        END, 2
    ) AS ec_percentage
FROM
    "DuesPayments"
LEFT JOIN
    "AssociationDetails"
ON
    "DuesPayments"."BILLING_ASSOCIATION_ID" = "AssociationDetails"."ASSOCIATION_ID"
LEFT JOIN (
    SELECT
        "BILLING_ASSOCIATION_ID",
        COUNT(*) AS total_payments
    FROM
        "DuesPayments"
    WHERE
        "BILLING_YEAR" = 2024
    GROUP BY
        "BILLING_ASSOCIATION_ID"
) AS total_payment_count
ON
    "DuesPayments"."BILLING_ASSOCIATION_ID" = total_payment_count."BILLING_ASSOCIATION_ID"
WHERE
    "DuesPayments"."EC_CONTROL_NUMBER" IS NULL
    AND "DuesPayments"."BILLING_YEAR" = 2024
GROUP BY
    "DuesPayments"."BILLING_ASSOCIATION_ID",
    "AssociationDetails"."ASSOCIATION_NAME",
    total_payment_count.total_payments
ORDER BY
    ec_percentage ASC;
