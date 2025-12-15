import pandas as pd
import os

# Load data
file_path = r"c:\Users\barun\Prediksi-Harga-Rumah\data\raw\DATA RUMAH.xlsx"
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:
    df = pd.read_excel(file_path)
    target = "HARGA"
    
    print("--- Statistik Harga (Original) ---")
    print(df[target].describe().apply(lambda x: format(x, 'f')))
    
    print("\n--- Sampel Data Termahal (Top 10) ---")
    print(df[target].nlargest(10))
    
    print("\n--- Sampel Data Termurah (Bottom 10) ---")
    print(df[target].nsmallest(10))

    Q1 = df[target].quantile(0.25)
    Q3 = df[target].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    print(f"\n--- Outlier thresholds ---")
    print(f"Batas Bawah: {lower_bound:,.0f}")
    print(f"Batas Atas: {upper_bound:,.0f}")
    
    outliers = df[(df[target] < lower_bound) | (df[target] > upper_bound)]
    print(f"\nJumlah Outliers: {len(outliers)} dari {len(df)} data ({len(outliers)/len(df)*100:.2f}%)")
