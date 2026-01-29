import pandas as pd
import os

file = os.path.join(os.path.dirname(__file__), '..', 'Book1.xlsx')
df = pd.read_excel(file, header=2)
print("Columns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
