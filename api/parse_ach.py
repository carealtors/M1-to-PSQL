import os
import pandas as pd
from sqlalchemy import create_engine

def parse_and_import(file_path, db_connection):
    # Read the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Extract metadata
    association_line = next(l for l in lines if "Association code" in l)
    bank_line = next(l for l in lines if "Bank ID" in l)
    transactions_line = next(l for l in lines if "Transactions for" in l)

    association_code, association_name = association_line.split(":", 1)[1].strip().split(" - ")
    bank_id, bank_name = bank_line.split(",", 1)[1].strip().split(" - ")
    date_range = transactions_line.split(",")[1].strip()
    start_date, end_date = date_range.split(" through ")

    # Insert metadata
    metadata_query = f"""
    INSERT INTO BankMetadata (AssociationCode, AssociationName, BankID, BankName, StartDate, EndDate)
    VALUES ('{association_code}', '{association_name}', {bank_id}, '{bank_name}', '{start_date}', '{end_date}')
    RETURNING MetadataID;
    """
    metadata_id = db_connection.execute(metadata_query).fetchone()[0]

    # Parse and import sections
    sections = {
        "Invoicing": [],
        "Manual Electronic Funds Transfer": [],
        "Chargeback Transfer": []
    }

    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith("Destination Association,ACH Settlement Number"):
            current_section = "Invoicing"
        elif line.startswith("Receiving Association,ACH Settlement Number"):
            current_section = "Manual Electronic Funds Transfer"
        elif line.startswith("EC Control Number,Transaction Number"):
            current_section = "Chargeback Transfer"
        elif current_section:
            sections[current_section].append(line)

    # Process sections
    for section, data in sections.items():
        if data:
            # Use the first line as headers and parse the data
            headers = data[0].split(",")
            rows = [row.split(",") for row in data[1:]]
            df = pd.DataFrame(rows, columns=headers)

            # Add MetadataID to the DataFrame
            df["MetadataID"] = metadata_id

            # Determine target table based on the section
            if section == "Invoicing":
                df.to_sql("Invoicing", db_connection, if_exists="append", index=False)
            elif section == "Manual Electronic Funds Transfer":
                df.to_sql("ManualEFT", db_connection, if_exists="append", index=False)
            elif section == "Chargeback Transfer":
                df.to_sql("Chargeback", db_connection, if_exists="append", index=False)

    print(f"Processed and imported data from {file_path}")


def process_all_files_in_folder(folder_path, db_connection):
    # Loop through all CSV files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing file: {file_path}")
            parse_and_import(file_path, db_connection)


if __name__ == "__main__":
    # Database connection
    engine = create_engine("postgresql://myusername:mypassword@localhost:5432/mydatabase")

    # Path to the folder containing CSV files
    folder_path = "/app/ach-data/"

    # Process all files in the folder
    process_all_files_in_folder(folder_path, engine)
