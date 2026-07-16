from pathlib import Path
import pandas as pd
import sys
from config import DATASETS

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def process_ipm(config):
    raw_folder = PROJECT_ROOT / config["raw_folder"]
    output_file = PROJECT_ROOT / config["output"]

    all_data = []

    for file in sorted(raw_folder.glob("ipm_*.xlsx")):
        year = int(file.stem.split("_")[1])

        df = pd.read_excel(file, header=None)

        df = df.iloc[1:].reset_index(drop=True)
        df.columns = ["Kabupaten_Kota", "IPM"]

        df["IPM"] = pd.to_numeric(df["IPM"], errors="coerce")
        # Hapus data provinsi
        df = df[df["Kabupaten_Kota"] != "Sumatera Utara"]

        # Hapus baris kosong
        df = df.dropna(subset=["Kabupaten_Kota", "IPM"])
        df["Tahun"] = year

        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)
    result = result[["Tahun", "Kabupaten_Kota", "IPM"]]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ {output_file.name} berhasil dibuat")


def process_penduduk(config):
    raw_folder = PROJECT_ROOT / config["raw_folder"]
    output_file = PROJECT_ROOT / config["output"]

    all_data = []

    for file in sorted(raw_folder.glob("penduduk_*.xlsx")):

        year = int(file.stem.split("_")[1])

        df = pd.read_excel(file, header=None)

        df = df.iloc[5:].reset_index(drop=True)

        df.columns = [
            "Kabupaten_Kota",
            "Jumlah_Penduduk",
            "Perempuan",
            "Laki_Laki"
        ]

        for col in [
            "Jumlah_Penduduk",
            "Perempuan",
            "Laki_Laki"
        ]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            # Hapus data provinsi
            df = df[~df["Kabupaten_Kota"].isin([
                "Sumatera Utara",
                "Provinsi Sumatera Utara"
            ])]

            # Hapus baris kosong
            df = df.dropna(subset=["Kabupaten_Kota"])

        df["Tahun"] = year

        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)

    result = result[
        [
            "Tahun",
            "Kabupaten_Kota",
            "Jumlah_Penduduk",
            "Perempuan",
            "Laki_Laki",
        ]
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ {output_file.name} berhasil dibuat")
    
def process_kemiskinan(config):

    raw_folder = PROJECT_ROOT / config["raw_folder"]
    output_file = PROJECT_ROOT / config["output"]

    all_data = []

    for file in sorted(raw_folder.glob("kemiskinan_*.xlsx")):

        year = int(file.stem.split("_")[1])

        df = pd.read_excel(file)
        
        if year == 2020:
            df = df.iloc[:, [0, 1, 2, 3]]
        else:
            df = df.iloc[:, [0, 1, 3, 5]]

        df.columns = [
            "Kabupaten_Kota",
            "Garis_Kemiskinan",
            "Jumlah_Penduduk_Miskin",
            "Persentase_Penduduk_Miskin"
]

        for col in [
            "Garis_Kemiskinan",
            "Jumlah_Penduduk_Miskin",
            "Persentase_Penduduk_Miskin"
        ]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            
            # Hapus data provinsi
            df = df[~df["Kabupaten_Kota"].isin([
                "Sumatera Utara",
                "Provinsi Sumatera Utara"
            ])]

            # Hapus baris kosong
            df = df.dropna(subset=[
                "Kabupaten_Kota",
                "Persentase_Penduduk_Miskin"
            ])
                        
            

        df["Tahun"] = year

        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)

    result = result[
        [
            "Tahun",
            "Kabupaten_Kota",
            "Garis_Kemiskinan",
            "Jumlah_Penduduk_Miskin",
            "Persentase_Penduduk_Miskin"
        ]
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ {output_file.name} berhasil dibuat")

def process_tpt(config):

    raw_folder = PROJECT_ROOT / config["raw_folder"]
    output_file = PROJECT_ROOT / config["output"]

    all_data = []

    for file in sorted(raw_folder.glob("tpt_*.xlsx")):

        year = int(file.stem.split("_")[1])

        df = pd.read_excel(file)

        df = df.iloc[:, [0,2,4]]

        df.columns = [
            "Kabupaten_Kota",
            "TPT",
            "TPAK"
        ]

        df["TPT"] = pd.to_numeric(df["TPT"], errors="coerce")
        df["TPAK"] = pd.to_numeric(df["TPAK"], errors="coerce")
        # Hapus data provinsi
        df = df[~df["Kabupaten_Kota"].isin([
            "Sumatera Utara",
            "Provinsi Sumatera Utara"
        ])]

        # Hapus baris kosong
        df = df.dropna(subset=["Kabupaten_Kota"])

        df["Tahun"] = year

        all_data.append(df)

    result = pd.concat(all_data, ignore_index=True)

    result = result[
        [
            "Tahun",
            "Kabupaten_Kota",
            "TPT",
            "TPAK"
        ]
    ]

    output_file.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_file, index=False, encoding="utf-8-sig")

    print(f"✅ {output_file.name} berhasil dibuat")
    
def main():

    if len(sys.argv) != 2:
        print("Contoh:")
        print("python scripts/etl.py ipm")
        print("python scripts/etl.py penduduk")
        print("python scripts/etl.py all")
        return

    dataset = sys.argv[1].lower()

    if dataset == "ipm":
        process_ipm(DATASETS["ipm"])

    elif dataset == "penduduk":
        process_penduduk(DATASETS["penduduk"])

    elif dataset == "kemiskinan":
        process_kemiskinan(DATASETS["kemiskinan"])
        
    elif dataset == "tpt":
        process_tpt(DATASETS["tpt"])
    
    elif dataset == "all":
        process_ipm(DATASETS["ipm"])
        process_penduduk(DATASETS["penduduk"])
        process_kemiskinan(DATASETS["kemiskinan"])
        process_tpt(DATASETS["tpt"])

    else:
        print("Dataset tidak ditemukan.")


if __name__ == "__main__":
    main()