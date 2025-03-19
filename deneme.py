import pandas as pd
import numpy as np


# Load the Excel file
file_path = 'Firma_katılımcı_liste/Sawo_Firmalar.xlsx'
df = pd.read_excel(file_path)

# Set the 'adres' column to null
df['Adres'] = np.nan

# Save the modified DataFrame back to the Excel file
df.to_excel(file_path, index=False)