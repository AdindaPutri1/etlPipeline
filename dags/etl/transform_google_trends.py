import pandas as pd
import os
from datetime import datetime, timezone

# 1. Lokasi folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(BASE_DIR, "dags/hasil data extract")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "dags/hasil data transform")
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# 2. Fungsi untuk mengubah timestamp ke format tanggal
def convert_timestamp(timestamp):
    try:
        # Menggunakan timezone-aware datetime dengan UTC
        return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error memproses timestamp: {timestamp} - {e}")
        return None

# 3. Fungsi untuk memproses file individual
def process_file(file_path, output_path):
    try:
        print(f"Memproses file: {file_path}")
        df = pd.read_csv(file_path)

        # Mengubah kolom 'time' menjadi 'date'
        if 'time' in df.columns:
            df['date'] = df['time'].apply(convert_timestamp)

        # Menghapus tanda kurung siku dari kolom 'value'
        if 'value' in df.columns:
            df['value'] = df['value'].str.strip("[]").astype(int)

        # Menghapus kolom yang tidak diperlukan
        columns_to_drop = ['time', 'formattedAxisTime', 'hasData', 'formattedValue', 'isPartial', 'formattedTime']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

        # Menyimpan hasil ke file baru
        df.to_csv(output_path, index=False)
        print(f"Hasil diproses disimpan di: {output_path}")
    except Exception as e:
        print(f"Error memproses file {file_path} - {e}")

# 4. Fungsi utama untuk memproses semua file
def process_all_files():
    for file_name in os.listdir(DATA_FOLDER):
        if (file_name.startswith("FemaleDaily") or file_name.startswith("GoogleTrends")) and file_name.endswith(".csv"):
            file_path = os.path.join(DATA_FOLDER, file_name)
            output_path = os.path.join(PROCESSED_FOLDER, file_name)
            process_file(file_path, output_path)

# 5. Main program
if __name__ == "__main__":
    process_all_files()
