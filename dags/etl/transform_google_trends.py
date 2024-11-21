import pandas as pd
from datetime import datetime, timezone
import os

# Fungsi untuk mengubah format tanggal dari 'Aug 21, 2024' menjadi '2024-08-21'
def convert_formatted_time(formatted_time):
    try:
        return datetime.strptime(formatted_time, "%b %d, %Y").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error memproses formattedTime: {formatted_time} - {e}")
        return None

# Fungsi untuk menghapus tanda kurung siku dan mengubah 'value' menjadi integer
def clean_value(value):
    try:
        # Menghapus kurung siku dan mengkonversi menjadi integer
        cleaned_value = value.strip("[]").split(",")[0]
        return int(cleaned_value)
    except Exception as e:
        print(f"Error memproses value: {value} - {e}")
        return None

# Fungsi untuk memproses file CSV
def process_file(file_path, output_path):
    try:
        print(f"Memproses file: {file_path}")
        
        # Membaca file CSV dengan mengabaikan baris yang bermasalah
        df = pd.read_csv(file_path, on_bad_lines='skip')

        # Mengubah kolom 'formattedTime' menjadi format tanggal yang diinginkan
        if 'formattedTime' in df.columns:
            df['date'] = df['formattedTime'].apply(convert_formatted_time)

        # Mengambil nilai dari kolom 'value' dan menghilangkan tanda kurung siku
        if 'value' in df.columns:
            df['value'] = df['value'].apply(clean_value)

        # Menghapus kolom yang tidak diperlukan
        columns_to_drop = ['time', 'formattedTime', 'formattedAxisTime', 'hasData', 'formattedValue']
        df = df.drop(columns=[col for col in columns_to_drop if col in df.columns], errors='ignore')

        # Menyimpan hasil ke file baru
        df.to_csv(output_path, index=False)
        print(f"Hasil diproses disimpan di: {output_path}")
    except Exception as e:
        print(f"Error memproses file {file_path} - {e}")

# Fungsi untuk memproses file terpilih
def process_all_files():
    DATA_FOLDER = "dags/hasil data extract"
    PROCESSED_FOLDER = "dags/hasil data transform"

    # Pastikan folder output ada
    os.makedirs(PROCESSED_FOLDER, exist_ok=True)

    # Daftar file yang ingin diproses
    selected_files = [
        "GoogleTrend_sunscreen_Azarine_interestOverTime.csv",
        "GoogleTrend_sunscreen_skin_aqua_interestOverTime.csv"
    ]
    
    # Memproses file yang ada dalam selected_files
    for file_name in selected_files:
        file_path = os.path.join(DATA_FOLDER, file_name)
        output_path = os.path.join(PROCESSED_FOLDER, file_name)
        if os.path.exists(file_path):  # Memastikan file ada
            process_file(file_path, output_path)
        else:
            print(f"File {file_name} tidak ditemukan di {DATA_FOLDER}.")

# Main program
if __name__ == "__main__":
    process_all_files()
