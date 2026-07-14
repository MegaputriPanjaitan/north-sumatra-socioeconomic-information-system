from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def save_csv(df, output_path):
    output = PROJECT_ROOT / output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False, encoding="utf-8-sig")
    print(f"✅ {output.name} berhasil dibuat")