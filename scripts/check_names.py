import pandas as pd
import os

# Load data
file_path = r"c:\Users\barun\Prediksi-Harga-Rumah\data\raw\DATA RUMAH.xlsx"
df = pd.read_excel(file_path)
print("--- NAMA RUMAH Samples ---")
print(df['NAMA RUMAH'].head(10))
