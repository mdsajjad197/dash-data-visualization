import pandas as pd
import glob
from datetime import datetime
from pathlib import Path


files = glob.glob("data/*.csv")

df_list = []

if not files:
    raise FileNotFoundError("No CSV files found in the data folder.")

for file in files:
    df = pd.read_csv(file)
    df_list.append(df)


final_df = pd.concat(df_list, ignore_index=True)
final_df.columns = final_df.columns.str.strip()

final_df = final_df[
    final_df["product"].str.lower().str.strip() == "pink morsel"
].copy()
final_df["price"] = final_df["price"].replace(r"[\$,]", "", regex=True).astype(float)
final_df["Sales"] = final_df["price"] * final_df["quantity"]
final_df = final_df[["Sales", "date", "region"]]

output_path = Path("output.csv")

try:
    final_df.to_csv(output_path, index=False)
except PermissionError:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(f"output_{timestamp}.csv")
    final_df.to_csv(output_path, index=False)
    print(
        "output.csv is locked or not writable. "
        f"Created {output_path} instead. Close output.csv if it is open in Excel."
    )


print(f"{output_path} created successfully")
print(final_df.head())
