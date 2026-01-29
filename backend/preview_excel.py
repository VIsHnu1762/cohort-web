import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Configuration
EXCEL_FILE = '../DTPB Cohort Session Name List of IInd Years to Circulate.xlsx'

# Read and display Excel structure
df = pd.read_excel(EXCEL_FILE)
print("=" * 80)
print("EXCEL FILE PREVIEW")
print("=" * 80)
print(f"\nTotal rows: {len(df)}")
print(f"\nColumn names:")
for i, col in enumerate(df.columns):
    print(f"  {i}: {col}")

print("\n" + "=" * 80)
print("FIRST 10 ROWS:")
print("=" * 80)
print(df.head(10).to_string())

print("\n" + "=" * 80)
print("DATA SAMPLE (first 5 non-null values per column):")
print("=" * 80)
for col in df.columns:
    values = df[col].dropna().head(5).tolist()
    print(f"\n{col}:")
    for v in values:
        print(f"  - {v}")
