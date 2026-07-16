DATASETS = {

    "ipm": {
        "raw_folder": "data/raw/pembangunan",
        "output": "data/processed/ipm_master.csv",
        "file_prefix": "ipm",
        "skip_rows": 1,
        "columns": [
            "Kabupaten_Kota",
            "IPM"
        ]
    },

    "penduduk": {
        "raw_folder": "data/raw/demografi",
        "output": "data/processed/penduduk_master.csv",
        "file_prefix": "penduduk",
        "skip_rows": 4,
        "columns": [
            "Kabupaten_Kota",
            "Jumlah_Penduduk",
            "Perempuan",
            "Laki_Laki"
        ]
    },

    "kemiskinan": {
        "raw_folder": "data/raw/kemiskinan",
        "output": "data/processed/kemiskinan_master.csv",
        "file_prefix": "kemiskinan"
    },
    
    "tpt": {
    "raw_folder": "data/raw/ketenagakerjaan",
    "output": "data/processed/tpt_master.csv"
},

}