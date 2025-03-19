import pandas as pd
import os
import glob

def combine_company_lists():
    """
    Combines all company xlsx files in the Firma_katılımcı_liste directory
    into a single file, merging "Katıldığı Fuar" information for companies
    that appear in multiple fairs, while avoiding duplicates.
    Sets 'Adres' field to null for AA fair companies.
    """
    # Get all xlsx files in the directory
    xlsx_path = 'Firma_katılımcı_liste/*.xlsx'
    all_files = glob.glob(xlsx_path)
    
    # Exclude the combined file if it exists
    combined_file = 'Firma_katılımcı_liste/Tüm_Firmalar_Birleşik.xlsx'
    all_files = [file for file in all_files if file != combined_file]
    
    if not all_files:
        print(f"No xlsx files found in the path: {xlsx_path}")
        return
    
    print(f"Found {len(all_files)} xlsx files to combine")
    
    # Initialize an empty list to store all dataframes
    all_dfs = []
    
    # Read each xlsx file and append to the list
    for file in all_files:
        try:
            df = pd.read_excel(file)
            fair_name = os.path.basename(file).split('_')[0]  # Extract fair name from filename
            print(f"Reading {fair_name} with {len(df)} companies")
            
            # Only keep the columns we need
            required_columns = [
                "Firma Adı", "Sektör", "Yetkili Ad-Soyad", "Unvan", 
                "Telefon", "Email", "Adres", "Website", "Katıldığı Fuar", "Ülke"
            ]
            
            # Ensure all required columns exist (fill with NaN if they don't)
            for col in required_columns:
                if col not in df.columns:
                    df[col] = pd.NA
            
            # Set the 'Adres' field to null for AA companies
            if 'AA' in fair_name:
                df['Adres'] = pd.NA
                print(f"Setting address to null for all companies in {fair_name}")
            
            # Only keep the required columns
            df = df[required_columns]
            
            all_dfs.append(df)
        except Exception as e:
            print(f"Error reading file {file}: {e}")
    
    if not all_dfs:
        print("No valid data found in any of the files")
        return
    
    # Combine all dataframes
    combined_df = pd.concat(all_dfs, ignore_index=True)
    
    # Group by company name and merge fair information
    result = pd.DataFrame(columns=combined_df.columns)
    
    # Group by company name
    grouped = combined_df.groupby("Firma Adı")
    
    for company, group in grouped:
        # Get the first row for this company
        first_row = group.iloc[0].copy()
        
        # If this company appears in multiple fairs, combine the fair names
        if len(group) > 1:
            # Collect all distinct fair names for this company
            fairs = group["Katıldığı Fuar"].dropna().unique()
            first_row["Katıldığı Fuar"] = ", ".join(fairs)
            
            # For other columns, take the first non-null value
            for col in first_row.index:
                if col != "Katıldığı Fuar" and col != "Firma Adı":
                    non_null_values = group[col].dropna()
                    if len(non_null_values) > 0:
                        first_row[col] = non_null_values.iloc[0]
        
        # Add the merged row to the result
        result = pd.concat([result, pd.DataFrame([first_row])], ignore_index=True)
    
    # Sort by company name
    result = result.sort_values(by="Firma Adı")
    
    # Save the combined data to a new Excel file
    output_path = 'Tüm_Firmalar_Birleşik.xlsx'
    result.to_excel(output_path, index=False)
    
    print(f"Successfully combined {len(all_dfs)} files into {output_path}")
    print(f"Total unique companies: {len(result)}")
    
    return result

if __name__ == "__main__":
    combine_company_lists()