import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Just preview the structure
EXCEL_FILE = '../DTPB Cohort Session Name List of IInd Years to Circulate.xlsx'

df = pd.read_excel(EXCEL_FILE, header=None)
print("=" * 80)
print("RAW EXCEL STRUCTURE")
print("=" * 80)
print("\nFirst 10 rows:")
print(df.head(10))
print("\n" + "=" * 80)
