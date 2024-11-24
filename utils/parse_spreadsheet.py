import pandas as pd

def find_table_and_export(input_file, output_file, expected_columns):
    """
    Process a spreadsheet, find the table headers, and export the table as CSV.

    :param input_file: Path to the input spreadsheet file (Excel format).
    :param output_file: Path to the output CSV file.
    :param expected_columns: List of expected column names to identify the table headers.
    """
    # Load the entire spreadsheet
    xl = pd.ExcelFile(input_file)

    # Loop through each sheet (if needed)
    for sheet_name in xl.sheet_names:
        print(f"Processing sheet: {sheet_name}")

        # Read the sheet into a DataFrame
        df = xl.parse(sheet_name, header=None)

        # Find the header row by checking for expected columns
        header_row = None
        for i, row in df.iterrows():
            # Check if the row contains all the expected column names
            if set(expected_columns).issubset(set(row)):
                header_row = i
                print(f"Found header at row {header_row} in sheet '{sheet_name}'")
                break

        if header_row is not None:
            # Re-read the DataFrame starting from the header row
            table_df = pd.read_excel(input_file, sheet_name=sheet_name, header=header_row)

            # Export the cleaned table to CSV
            table_df.to_csv(output_file, index=False)
            print(f"Table exported to {output_file}")
            return

    print("No valid table found with the expected columns.")


# Define the expected column names for the table
expected_columns = [
    "ActionCodes",
    "Committee",
    "CommitteeCode",
    "CommitteeMemberStatus",
    "CommitteePositionTitle",
    "Compnayy",
    "EffectiveDate",
    "Email",
    "FirstName",
    "Id",
    "LastName",
    "MajorKey",
    "MobilePhone",
    "Note",
    "Position",
    "PrimaryLocalAssociationId",
    "ProductCode",
    "Rank",
    "Seqn",
    "TermBegin",
    "TermEnd",
    "TermYear",
    "ThruDate",
    "Title",
    "WorkPhone",
    "AssociationName",
    "Region"
]

# Path to the input Excel file
input_file = "/app/ach-data/my_spreadsheet.xlsx"
# Path to the output CSV file
output_file = "/app/ach-data/my_spreadsheet.csv"

# Call the function
find_table_and_export(input_file, output_file, expected_columns)
