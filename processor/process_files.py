import os
import psycopg2
import glob
from multiprocessing import Pool

# Get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
M1_DATA_DIR = os.getenv("M1_DATA_DIR")

def import_file_to_db(args):
    """
    Import a single file into the corresponding table.
    """
    file_path, table_name = args
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Construct SQL COPY command
        with open(file_path, 'r') as f:
            cur.copy_expert(
                f"COPY {table_name} FROM STDIN WITH (FORMAT csv, DELIMITER '|', HEADER true)", f
            )

        conn.commit()
        cur.close()
        conn.close()
        print(f"Successfully imported {file_path} into {table_name}")
    except Exception as e:
        print(f"Error importing {file_path}: {e}")

def main():
    if not M1_DATA_DIR:
        print("M1_DATA_DIR not set")
        exit(1)

    # List all M1 files in the directory
    files = glob.glob(os.path.join(M1_DATA_DIR, "*.m1"))

    tasks = []
    for file_path in files:
        file_name = os.path.basename(file_path)

        # Determine table name based on file name
        if "DuesPayments" in file_name:
            table_name = "DuesPayments"
        elif "MemberExtract" in file_name:
            table_name = "MemberExtract"
        elif "OfficeExtract" in file_name:
            table_name = "OfficeExtract"
        elif "MemberSecondaryExtract" in file_name:  
            table_name = "MemberSecondaryExtract"
        else:
            print(f"Unknown file type: {file_name}")
            continue

        tasks.append((file_path, table_name))

    # Use multiprocessing for parallel imports
    with Pool(processes=os.cpu_count()) as pool:
        pool.map(import_file_to_db, tasks)

if __name__ == "__main__":
    main()
