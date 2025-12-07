import pandas as pd
import re

def markdown_table_to_dataframe(filepath, check_duplicates_column=None):
    """
    Convert a markdown table from a file to a pandas DataFrame.
    
    Parameters:
    -----------
    filepath : str
        Path to the .md file containing a markdown table
    check_duplicates_column : str, optional
        If provided, check for and print duplicates in this column
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing the parsed markdown table
    
    Raises:
    -------
    FileNotFoundError
        If the file doesn't exist
    ValueError
        If no valid markdown table is found in the file
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content into lines
    lines = content.strip().split('\n')
    
    # Find table lines (non-empty lines that contain |)
    table_lines = [line for line in lines if line.strip() and '|' in line]
    
    if len(table_lines) < 2:
        raise ValueError("No valid markdown table found in file")
    
    # Parse header
    header = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
    
    # Skip the separator line (second line with dashes)
    data_lines = table_lines[2:]
    
    # Parse data rows
    data = []
    for line in data_lines:
        # Split by | and remove first and last empty elements
        cells = line.split('|')[1:-1]
        row = [cell.strip() for cell in cells]
        data.append(row)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=header)
    
    # Check for duplicates if requested
    if check_duplicates_column:
        if check_duplicates_column not in df.columns:
            print(f"⚠️  WARNING: Column '{check_duplicates_column}' not found. Available columns: {list(df.columns)}")
        else:
            # Normalize values for duplicate checking
            normalized_values = df[check_duplicates_column].str.strip().str.lower()
            duplicates = normalized_values[normalized_values.duplicated(keep=False)]
            
            if len(duplicates) > 0:
                unique_dups = duplicates.unique()
                print(f"⚠️  Found {len(duplicates)} duplicate values in column '{check_duplicates_column}':")
                for dup in unique_dups:
                    count = (normalized_values == dup).sum()
                    # Get the original values (not normalized) for display
                    original_values = df[df[check_duplicates_column].str.strip().str.lower() == dup][check_duplicates_column].tolist()
                    print(f"   - '{original_values[0]}' appears {count} times")
            else:
                print(f"✓ No duplicates found in column '{check_duplicates_column}'")
    
    return df


def compare_tables(reference_filepath, incoming_filepath, column_name):
    """
    Compare two csv tables and return only new rows from the incoming table.
    
    Returns rows from the incoming table where the specified column value
    doesn't already exist in the reference table.
    
    Parameters:
    -----------
    reference_filepath : str
        Path to the reference .csv file
    incoming_filepath : str
        Path to the incoming .csvß file
    column_name : str
        Name of the column to compare on (must exist in both tables)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame containing only the new rows from the incoming table
    
    Raises:
    -------
    ValueError
        If the specified column doesn't exist in one or both tables
    """
    # Load both tables
    ref_df = pd.read_csv(reference_filepath)
    incoming_df = pd.read_csv(incoming_filepath)
    
    # Check if column exists in both tables
    if column_name not in ref_df.columns:
        raise ValueError(f"Column '{column_name}' not found in reference table. Available columns: {list(ref_df.columns)}")
    if column_name not in incoming_df.columns:
        raise ValueError(f"Column '{column_name}' not found in incoming table. Available columns: {list(incoming_df.columns)}")
    
    # Normalize values: strip whitespace and convert to lowercase for comparison
    ref_values = ref_df[column_name].str.strip().str.lower()
    incoming_values = incoming_df[column_name].str.strip().str.lower()
    
    # Check for duplicates in incoming table
    duplicates = incoming_values[incoming_values.duplicated(keep=False)]
    if len(duplicates) > 0:
        unique_dups = duplicates.unique()
        print(f"⚠️  WARNING: Incoming table has {len(duplicates)} duplicate values in column '{column_name}':")
        for dup in unique_dups:
            count = (incoming_values == dup).sum()
            print(f"   - '{dup}' appears {count} times")
    
    # Find rows that already exist in reference
    existing_mask = incoming_values.isin(ref_values)
    existing_values = incoming_df[existing_mask][column_name].str.strip().str.lower().unique()
    
    if len(existing_values) > 0:
        print(f"\n📋 Already exist in reference ({len(existing_values)} unique values):")
        for val in existing_values:
            # Get the original value (not normalized) for display
            original_val = incoming_df[incoming_df[column_name].str.strip().str.lower() == val][column_name].iloc[0]
            print(f"   - '{original_val}'")
    
    # Find new rows (values not in reference)
    mask = ~incoming_values.isin(ref_values)
    new_rows = incoming_df[mask].drop_duplicates(subset=[column_name])
    
    # Print summary
    num_duplicates = len(incoming_df) - len(incoming_df.drop_duplicates(subset=[column_name]))
    num_existing = len(existing_values)
    
    print(f"\n📊 Summary:")
    print(f"   - Total rows in incoming table: {len(incoming_df)}")
    print(f"   - Duplicates in incoming table: {num_duplicates}")
    print(f"   - Already exist in reference: {num_existing}")
    print(f"   - New unique rows: {len(new_rows)}")
    
    return new_rows