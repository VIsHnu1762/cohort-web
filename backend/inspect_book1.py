import pandas as pd
import os

file = os.path.join(os.path.dirname(__file__), '..', 'Book1.xlsx')
df = pd.read_excel(file, header=None)
print("First 10 rows:")
print(df.head(10))
print("\nShape:", df.shape)
