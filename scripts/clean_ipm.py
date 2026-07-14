from pathlib import Path
import pandas as pd

# Folder project
RAW_FOLDER = Path("data/raw/pembangunan")
OUTPUT_FOLDER = Path("data/processed")

OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

all_data = []

# Membaca semua file ipm_*.xlsx
for file in sorted(RAW_FOLDER.glob("ipm_*.xlsx")):

    # Ambil tahun dari nama file
    year = file.stem.split("_")[1]

    # Baca Excel tanpa header
    df = pd.read_excel(file, header=None)

    # Ambil data mulai baris ke-4
    df = df.iloc[3:].reset_index(drop=True)

    # Rename kolom
    df.columns = ["Kabupaten_Kota", "IPM"]

    # Tambahkan kolom tahun
    df["Tahun"] = int(year)

    # Ubah "-" menjadi kosong
    df["IPM"] = df["IPM"].replace("-", pd.NA)

    # Ubah ke numerik
    df["IPM"] = pd.to_numeric(df["IPM"], errors="coerce")

    all_data.append(df)

# Gabungkan semua tahun
ipm_master = pd.concat(all_data, ignore_index=True)

# Urutkan kolom
ipm_master = ipm_master[["Tahun", "Kabupaten_Kota", "IPM"]]

# Simpan
output_file = OUTPUT_FOLDER / "ipm_master.csv"
ipm_master.to_csv(output_file, index=False, encoding="utf-8-sig")

print(f"Berhasil membuat: {output_file}")
print(ipm_master.head())