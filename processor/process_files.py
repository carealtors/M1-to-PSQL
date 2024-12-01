import os
import psycopg2
import glob
import csv
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
M1_DATA_DIR = os.getenv("M1_DATA_DIR")
ACH_DATA_DIR = os.getenv("ACH_DATA_DIR")


def process_m1_files():

    """Process and import M1 files into the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        m1_files = glob.glob(os.path.join(M1_DATA_DIR, "*.m1"))

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

def extract_bank_metadata(file_path, cur):
    """Extract and insert bank metadata from the top portion of the ACH file."""
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
            print(f"Error parsing Bank ID line: {bank_line} - {e}")
            metadata["BankID"] = None
            metadata["BankName"] = None

        # Check if all necessary metadata fields are present
        if metadata["AssociationCode"] and metadata.get("BankID") is not None:
            cur.execute(
                """
                INSERT INTO "BankMetadata" ("AssociationCode", "AssociationName", "BankID", "BankName")
                VALUES (%s, %s, %s, %s)
                """,
                (
                    metadata["AssociationCode"],
                    metadata["AssociationName"],
                    metadata["BankID"],
                    metadata["BankName"],
                ),
            )
            print(f"Inserted metadata from {file_path}: {metadata}")
        else:
            print(f"No valid metadata found in {file_path}.")


def process_ach_files():
    """Process and import ACH files into the database."""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        ach_files = glob.glob(os.path.join(ACH_DATA_DIR, "*.csv"))

        for file_path in ach_files:
            print(f"Processing ACH file: {file_path}")

            # Extract and insert bank metadata
            extract_bank_metadata(file_path, cur)

        conn.commit()
        cur.close()
        conn.close()
        print("ACH files processed successfully!")
    except Exception as e:
        print(f"Error processing ACH files: {e}")


if __name__ == "__main__":
    print("Starting data processing...")
    #process_m1_files()  # Process M1 files
    process_ach_files()  # Process ACH files
    print("Data processing complete!")
