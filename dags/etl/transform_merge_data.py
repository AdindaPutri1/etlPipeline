import os
import pandas as pd

# 1. Tentukan jalur file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = "dags/hasil data transform"
MERGE_FOLDER = "dags/hasil data transform"

# 2. Daftar pasangan file yang akan digabungkan
FILE_COMBINATIONS = [
    {
        "female_daily_file": "FemaleDaily_Sunscreen Azarine.csv",
        "pytrends_file": "GoogleTrend_sunscreen_Azarine_interestOverTime.csv",
        "output_name": "Merged_Sunscreen Azarine.csv"
    },
    {
        "female_daily_file": "FemaleDaily_Sunscreen Skinaqua.csv",
        "pytrends_file": "GoogleTrend_sunscreen_skin_aqua_interestOverTime.csv",
        "output_name": "Merged_Sunscreen Skinaqua.csv"
    },
]

# Fungsi untuk membaca file CSV
def read_csv_file(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File tidak ditemukan: {file_path}")
        return None

# Fungsi untuk menggabungkan dua DataFrame berdasarkan kolom 'date'
def merge_dataframes(female_df, pytrends_df):
    if female_df is not None and pytrends_df is not None:
        return pd.merge(female_df, pytrends_df, on="date", how="inner")  # Gunakan 'outer' jika ingin semua data muncul
    else:
        print("Salah satu DataFrame tidak tersedia untuk penggabungan.")
        return None

# Fungsi untuk menyimpan DataFrame yang digabungkan
def save_merged_dataframe(merged_df, output_file_path):
    if merged_df is not None:
        merged_df.to_csv(output_file_path, index=False)
        print(f"Hasil gabungan disimpan di: {output_file_path}")
    else:
        print("Data gabungan kosong, tidak dapat menyimpan file.")

# Fungsi utama untuk memproses semua kombinasi file
def process_combinations(file_combinations):
    for combination in file_combinations:
        female_file_path = os.path.join(DATA_FOLDER, combination["female_daily_file"])
        pytrends_file_path = os.path.join(DATA_FOLDER, combination["pytrends_file"])
        output_file_path = os.path.join(MERGE_FOLDER, combination["output_name"])
        
        print(f"Menggabungkan: {combination['female_daily_file']} + {combination['pytrends_file']}")

        # Baca file CSV
        female_df = read_csv_file(female_file_path)
        pytrends_df = read_csv_file(pytrends_file_path)

        # Gabungkan data
        merged_df = merge_dataframes(female_df, pytrends_df)

        # Simpan hasil gabungan
        save_merged_dataframe(merged_df, output_file_path)

# Fungsi main untuk menjalankan program
def merge():
    try:
        process_combinations(FILE_COMBINATIONS)
    except Exception as e:
        print(f"Error saat memproses data: {e}")

# Jalankan program
if __name__ == "__main__":
    merge()
