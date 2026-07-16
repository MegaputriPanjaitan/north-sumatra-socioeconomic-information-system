import pdfplumber
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

pdf_folder = PROJECT_ROOT / "data/source_documents/ipm"

all_data = []

for pdf_file in sorted(pdf_folder.glob("*.pdf")):

    tahun = int(pdf_file.stem.split("_")[1])

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            table = page.extract_table()

            if table is None:
                continue

            df = pd.DataFrame(table)

            if "Kabupaten" not in str(df.iloc[0]):
                continue

            df.columns = df.iloc[0]
            df = df.iloc[1:]

            df = df.iloc[:,0:5]

            df.columns = [
                "Kabupaten_Kota",
                "UHH",
                "HLS",
                "RLS",
                "Pengeluaran"
            ]

            df["Tahun"] = tahun

            all_data.append(df)

result = pd.concat(all_data, ignore_index=True)

result.to_csv(
    PROJECT_ROOT/"data/processed/ipm_components_master.csv",
    index=False,
    encoding="utf-8-sig"
)

print(result.head())