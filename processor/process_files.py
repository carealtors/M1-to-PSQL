import os
import psycopg2
import glob
import csv
import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
M1_DATA_DIR = os.getenv("M1_DATA_DIR")
ACH_DATA_DIR = os.getenv("ACH_DATA_DIR")

# Set up logging to print to console
logging.basicConfig(
    level=logging.WARNING,  # Set the logging level
    format="%(asctime)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S",  # Date format
    handlers=[logging.StreamHandler()]  # Use StreamHandler for console output
)

def process_association_data():
    """Process and import associations.csv into the database."""
    associations_file = os.path.join(M1_DATA_DIR, "808_AssociationDirectoryExtract.csv")
    if not os.path.exists(associations_file):
        print("No associations.csv file found in the m1-data folder. Skipping...")
        return

    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = False  # Explicit transaction management
        cur = conn.cursor()

        print(f"Processing association data from {associations_file}...")
        with open(associations_file, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            # Columns must match the database schema
            columns = reader.fieldnames
            placeholders = ", ".join(["%s"] * len(columns))
            query = f"""
                INSERT INTO "AssociationDetails" ({', '.join(f'"{col}"' for col in columns)}) 
                VALUES ({placeholders})
            """

            for row_num, row in enumerate(reader, start=1):
                try:
                    # Handle empty strings and convert them to None
                    values = [
                        row[col].strip() if row[col].strip() else None for col in columns
                    ]

                    # Convert dates and datetimes
                    for idx, col in enumerate(columns):
                        if col.endswith("_DATE") or col.endswith("_DATETIME"):
                            if values[idx]:
                                try:
                                    values[idx] = datetime.strptime(
                                        values[idx], "%Y-%m-%d %H:%M:%S.%f"
                                    )
                                except ValueError:
                                    try:
                                        values[idx] = datetime.strptime(
                                            values[idx], "%Y-%m-%d"
                                        )
                                    except ValueError:
                                        values[idx] = None

                    # Execute the query
                    cur.execute(query, values)
                except Exception as e:
                    logging.warning(f"Failed to insert row {row_num}: {row} - Error: {e}")
                    conn.rollback()  # Roll back on error to maintain consistency
                else:
                    conn.commit()  # Commit if successful

        cur.close()
        conn.close()
        print("Association data processed successfully!")
    except Exception as e:
        logging.error(f"Error processing association data: {e}")


def process_m1_files():
    """Process and import M1 files into the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        m1_files = glob.glob(os.path.join(M1_DATA_DIR, "*.m1"))
        print(f"Files found in M1 directory: {m1_files}")

        for file_path in m1_files:
            file_name = os.path.basename(file_path)

            # Map file names to database table names
            if "DuesPayments" in file_name:
                table_name = '"DuesPayments"'
            elif "MemberExtract" in file_name:
                table_name = '"MemberExtract"'
            elif "OfficeExtract" in file_name:
                table_name = '"OfficeExtract"'
            elif "MemberSecondaryExtract" in file_name:
                table_name = '"MemberSecondaryExtract"'
            else:
                print(f"Unknown file type: {file_name}")
                continue

            print(f"Importing {file_name} into {table_name}...")
            with open(file_path, "r") as file:
                cur.copy_expert(
                    f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER '|', HEADER true)", file
                )

        conn.commit()
        cur.close()
        conn.close()
        print("M1 files imported successfully!")
    except Exception as e:
        print(f"Error importing M1 files: {e}")


def process_invoicing_section(file_path, cur, bank_id):
    """Process the Invoicing section of the ACH file and insert data into the Invoicing table."""
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            # Skip lines until the invoicing section starts (line 8 is the header row)
            for _ in range(8):
                next(file)

            # Define the hard-coded headers
            headers = [
                "Destination Association",
                "ACH Settlement Number",
                "EC Control Number",
                "Member Name",
                "Member ID",
                "Billing Year",
                "Gross Amount of Invoice",
                "Association Portion of Invoice",
                "Transaction Fee on Assoc Portion",
                "Net Association Portion",
            ]

            # Use csv.reader to parse the file correctly
            reader = csv.reader(file)
            for row_num, values in enumerate(reader, start=9):  # Start at line 9 for error tracking
                # Stop processing if a blank line is encountered
                if not values or all(not value.strip() for value in values):
                    logging.warning(f"Blank line at {file_path}, line {row_num}. Stopping section processing.")
                    break

                # Ensure there are enough columns to match headers
                if len(values) != len(headers):
                    logging.warning(f"Malformed row at {file_path}, line {row_num}: {values}")
                    continue

                # Map values to columns
                row = dict(zip(headers, values))

                try:
                    # Insert into the database
                    cur.execute(
                        """
                        INSERT INTO "Invoicing" (
                            "BankID",
                            "DestinationAssociation",
                            "ACHSettlementNumber",
                            "EC_CONTROL_NUMBER",
                            "MemberName",
                            "MemberID",
                            "BillingYear",
                            "GrossAmount",
                            "AssociationPortion",
                            "TransactionFee",
                            "NetAssociationPortion"
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            bank_id,
                            row["Destination Association"],
                            row["ACH Settlement Number"],
                            row["EC Control Number"],
                            row["Member Name"],
                            int(row["Member ID"]) if row["Member ID"] else None,
                            int(row["Billing Year"]) if row["Billing Year"] else None,
                            float(row["Gross Amount of Invoice"].replace("$", "").replace(",", "")) if row["Gross Amount of Invoice"] else None,
                            float(row["Association Portion of Invoice"].replace("$", "").replace(",", "")) if row["Association Portion of Invoice"] else None,
                            float(row["Transaction Fee on Assoc Portion"].replace("$", "").replace(",", "")) if row["Transaction Fee on Assoc Portion"] else None,
                            float(row["Net Association Portion"].replace("$", "").replace(",", "")) if row["Net Association Portion"] else None,
                        ),
                    )
                except Exception as e:
                    logging.warning(f"Failed to insert row at {file_path}, line {row_num}: {row} - Error: {e}")
    except Exception as e:
        logging.warning(f"Error processing invoicing section in {file_path}: {e}")

def extract_bank_metadata(file_path, cur):
    """Extract and insert bank metadata from the top portion of the ACH file."""
    try:
        with open(file_path, "r", encoding='utf-8-sig') as file:
            lines = [next(file) for _ in range(3)]  # Read the first 3 lines

            # Line 2: Association code and name
            association_line = lines[1].strip()
            association_parts = association_line.split("-", 1)
            metadata = {
                "AssociationCode": association_parts[0].strip(),
                "AssociationName": association_parts[1].strip() if len(association_parts) > 1 else None,
            }

            # Line 3: Bank ID and name
            bank_line = lines[2].strip().replace("Bank ID:,", "Bank ID:")  # Clean up commas
            try:
                bank_data = bank_line.split(":", 1)[1].strip()  # Extract data after "Bank ID:"
                bank_parts = bank_data.split("-", 1)
                metadata["BankID"] = int(bank_parts[0].strip())  # Numeric Bank ID
                metadata["BankName"] = bank_parts[1].strip() if len(bank_parts) > 1 else None
            except (IndexError, ValueError) as e:
                logging.warning(f"Error parsing Bank ID line in {file_path}: {bank_line} - {e}")
                metadata["BankID"] = None
                metadata["BankName"] = None

            # Check if the BankID already exists in the database
            if metadata.get("BankID") is not None:
                cur.execute(
                    """
                    SELECT "BankID" FROM "BankMetadata" WHERE "BankID" = %s
                    """,
                    (metadata["BankID"],),
                )
                existing_bank = cur.fetchone()

                if existing_bank:
                    # BankID exists, return it
                    logging.info(f"BankID {metadata['BankID']} already exists. Skipping insertion.")
                    return existing_bank[0]
                else:
                    # Insert metadata into the database if valid
                    cur.execute(
                        """
                        INSERT INTO "BankMetadata" ("AssociationCode", "AssociationName", "BankID", "BankName")
                        VALUES (%s, %s, %s, %s)
                        RETURNING "BankID"
                        """,
                        (
                            metadata["AssociationCode"],
                            metadata["AssociationName"],
                            metadata["BankID"],
                            metadata["BankName"],
                        ),
                    )
                    bank_id = cur.fetchone()[0]
                    return bank_id
            else:
                logging.warning(f"Invalid metadata in {file_path}.")
                return None
    except Exception as e:
        logging.warning(f"Error extracting bank metadata in {file_path}: {e}")
        return None


def process_manual_etf_section(file_path, cur, bank_id):
    """Process the Manual EFT section of the ACH file and insert data into the ManualEFT table."""
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            found_manual_etf = False
            row_num = 0

            for line in file:
                row_num += 1
                line = line.strip()

                # Look for the start of the Manual ETF section
                if "Manual Electronic Funds Transfer" in line:
                    found_manual_etf = True
                    logging.info(f"Found Manual ETF section in {file_path} at line {row_num}.")
                    next(file)  # Skip the header line
                    break

            if not found_manual_etf:
                logging.warning(f"No Manual ETF section found in {file_path}.")
                return

            headers = [
                "Receiving Association",
                "ACH Settlement Number",
                "EC Control Number",
                "Destination Organization",
                "",
                "Amount",
            ]

            reader = csv.reader(file)
            for row_num, values in enumerate(reader, start=row_num + 1):
                # Stop processing if a blank line is encountered
                if not values or all(not value.strip() for value in values):
                    logging.info(f"Blank line encountered in {file_path} at line {row_num}. Stopping Manual ETF processing.")
                    break

                # Ensure there are enough columns to match headers
                if len(values) != len(headers):
                    logging.warning(f"Malformed row at {file_path}, line {row_num}: {values}")
                    continue

                # Map values to columns, skipping the blank column
                row = {
                    "Receiving Association": values[0],
                    "ACH Settlement Number": values[1],
                    "EC Control Number": values[2],
                    "Destination Organization": values[3],
                    "Amount": values[5],
                }

                try:
                    # Insert into the database
                    cur.execute(
                        """
                        INSERT INTO "ManualEFT" (
                            "BankID",
                            "ReceivingAssociation",
                            "ACHSettlementNumber",
                            "EC_CONTROL_NUMBER",
                            "DestinationOrganization",
                            "Amount"
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        (
                            bank_id,
                            row["Receiving Association"],
                            row["ACH Settlement Number"],
                            row["EC Control Number"],
                            row["Destination Organization"],
                            float(row["Amount"].replace("$", "").replace(",", "")) if row["Amount"] else None,
                        ),
                    )
                except Exception as e:
                    logging.warning(f"Failed to insert row at {file_path}, line {row_num}: {row} - Error: {e}")

    except Exception as e:
        logging.warning(f"Error processing Manual EFT section in {file_path}: {e}")

def process_external_interface_section(file_path, cur, bank_id):
    """Process the External Interface section of the ACH file and insert data into the ExternalInterface table."""
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            found_external_interface = False
            row_num = 0

            for line in file:
                row_num += 1
                line = line.strip()

                # Look for the start of the External Interface section
                if "External Interface" in line:
                    found_external_interface = True
                    logging.info(f"Found External Interface section in {file_path} at line {row_num}.")
                    next(file)  # Skip the header line
                    break

            if not found_external_interface:
                logging.warning(f"No External Interface section found in {file_path}.")
                return

            headers = [
                "Destination Association",
                "ACH Settlement Number",
                "EC Control Number",
                "Member Name",
                "Member ID",
                "Billing Year",
                "Gross Amount of Invoice",
                "Association Portion of Amount",
                "Transaction Fee on Assoc Portion",
                "Net Association Portion",
                "Account Name"
            ]

            reader = csv.reader(file)
            for row_num, values in enumerate(reader, start=row_num + 1):
                # Stop processing if a blank line is encountered
                if not values or all(not value.strip() for value in values):
                    logging.info(f"Blank line encountered in {file_path} at line {row_num}. Stopping External Interface processing.")
                    break

                # Ensure there are enough columns to match headers
                if len(values) != len(headers):
                    logging.warning(f"Malformed row at {file_path}, line {row_num}: {values}")
                    continue

                # Map values to columns
                row = dict(zip(headers, values))

                try:
                    # Insert into the database
                    cur.execute(
                        """
                        INSERT INTO "ExternalInterface" (
                            "BankID",
                            "DestinationAssociation",
                            "ACHSettlementNumber",
                            "EC_CONTROL_NUMBER",
                            "MemberName",
                            "MemberID",
                            "BillingYear",
                            "GrossAmountOfInvoice",
                            "AssociationPortionOfAmount",
                            "TransactionFeeOnAssocPortion",
                            "NetAssociationPortion",
                            "AccountName"
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            bank_id,
                            row["Destination Association"],
                            row["ACH Settlement Number"],
                            row["EC Control Number"],
                            row["Member Name"],
                            int(row["Member ID"]) if row["Member ID"] else None,
                            int(row["Billing Year"]) if row["Billing Year"] else None,
                            float(row["Gross Amount of Invoice"].replace("$", "").replace(",", "")) if row["Gross Amount of Invoice"] else None,
                            float(row["Association Portion of Amount"].replace("$", "").replace(",", "")) if row["Association Portion of Amount"] else None,
                            float(row["Transaction Fee on Assoc Portion"].replace("$", "").replace(",", "")) if row["Transaction Fee on Assoc Portion"] else None,
                            float(row["Net Association Portion"].replace("$", "").replace(",", "")) if row["Net Association Portion"] else None,
                            row["Account Name"]
                        ),
                    )
                except Exception as e:
                    logging.warning(f"Failed to insert row at {file_path}, line {row_num}: {row} - Error: {e}")

    except Exception as e:
        logging.warning(f"Error processing External Interface section in {file_path}: {e}")


def process_chargeback_section(file_path, cur, bank_id):
    """Process the Chargeback section of the ACH file and insert data into the Chargeback table."""
    try:
        with open(file_path, "r", encoding="utf-8-sig") as file:
            found_chargeback = False
            row_num = 0

            for line in file:
                row_num += 1
                line = line.strip()

                # Look for the start of the Chargeback section
                if "Chargeback Transfer" in line:
                    found_chargeback = True
                    logging.info(f"Found Chargeback section in {file_path} at line {row_num}.")
                    next(file)  # Skip the header line
                    break

            if not found_chargeback:
                logging.warning(f"No Chargeback section found in {file_path}.")
                return

            headers = [
                "EC Control Number",
                "Transaction Number",
                "Destination Organization",
                "Amount",
            ]

            reader = csv.reader(file)
            for row_num, values in enumerate(reader, start=row_num + 1):
                # Stop processing if a blank line is encountered
                if not values or all(not value.strip() for value in values):
                    logging.info(f"Blank line encountered in {file_path} at line {row_num}. Stopping Chargeback processing.")
                    break

                # Ensure there are enough columns to match headers
                if len(values) != len(headers):
                    logging.warning(f"Malformed row at {file_path}, line {row_num}: {values}")
                    continue

                # Map values to columns
                row = dict(zip(headers, values))

                try:
                    # Insert into the database
                    cur.execute(
                        """
                        INSERT INTO "Chargeback" (
                            "BankID",
                            "EC_CONTROL_NUMBER",
                            "TransactionNumber",
                            "DestinationOrganization",
                            "Amount"
                        ) VALUES (%s, %s, %s, %s, %s)
                        """,
                        (
                            bank_id,
                            row["EC Control Number"],
                            row["Transaction Number"],
                            row["Destination Organization"],
                            float(row["Amount"].replace("$", "").replace(",", "")) if row["Amount"] else None,
                        ),
                    )
                except Exception as e:
                    logging.warning(f"Failed to insert row at {file_path}, line {row_num}: {row} - Error: {e}")

    except Exception as e:
        logging.warning(f"Error processing Chargeback section in {file_path}: {e}")


def process_ach_files():
    """Process and import ACH files into the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        ach_files = glob.glob(os.path.join(ACH_DATA_DIR, "*.csv"))
        print(f"Files found in ACH directory: {ach_files}")

        for file_path in ach_files:
            try:
                print(f"Processing ACH file: {file_path}")
                # Extract and insert bank metadata
                bank_id = extract_bank_metadata(file_path, cur)

                if bank_id is not None:
                    # Process invoicing section
                    process_invoicing_section(file_path, cur, bank_id)
                    # Process Manual EFT section
                    process_manual_etf_section(file_path, cur, bank_id)
                    # Process External Interface section
                    process_external_interface_section(file_path, cur, bank_id)
                    # Process Chargeback section
                    process_chargeback_section(file_path, cur, bank_id)
                else:
                    logging.warning(f"Skipping file {file_path} due to invalid bank metadata.")
            except Exception as e:
                logging.warning(f"Error processing file {file_path}: {e}")

        conn.commit()
        cur.close()
        conn.close()
        print("ACH files processed successfully!")
    except Exception as e:
        logging.warning(f"Error processing ACH files: {e}")



if __name__ == "__main__":
   
    #Check process flags 
    process_m1 = os.getenv("PROCESS_M1", "0").strip() == "1"
    process_ach = os.getenv("PROCESS_ACH", "0").strip() == "1"
    print("Starting data processing...")

    if process_m1:
        print("Processing M1 files...")
        process_association_data()
        process_m1_files()
    else:
        print("Skipping M1 file processing as PROCESS_M1 is not set to 1.")

    if process_ach:
        print("Processing ACH files...")
        process_ach_files()
    else:
        print("Skipping ACH file processing as PROCESS_ACH is not set to 1.")

    print("Data processing complete!")
    