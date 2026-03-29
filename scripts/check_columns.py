import pandas as pd
import os

# Load data
file_path = r"c:\Users\barun\Prediksi-Harga-Rumah\data\raw\DATA RUMAH.xlsx"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    df = pd.read_excel(file_path)
    print("--- Columns ---")
    print(df.columns.tolist())
    
    # Check if there is any location-like column
    print("\n--- Sample Data (First 3 rows) ---")
    print(df.head(3))
