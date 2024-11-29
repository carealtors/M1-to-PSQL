import os
from dotenv import load_dotenv
import psycopg2
import csv

# Load environment variables from .env file
load_dotenv()

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
M1_FILES_DIR = os.getenv("M1_DATA_DIR")
ACH_FILES_DIR = os.getenv("ACH_DATA_DIR")

def process_m1_files():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    for filename in os.listdir(M1_FILES_DIR):
        if filename.endswith(".m1"):
            filepath = os.path.join(M1_FILES_DIR, filename)
            print(f"Processing file: {filename}")
            with open(filepath, "r") as file:
                reader = csv.reader(file, delimiter="|")
                headers = next(reader)
                # Insert logic remains the same as earlier...

    conn.commit()
    cur.close()
    conn.close()
    print("Processing complete!")

if __name__ == "__main__":
    process_m1_files()
