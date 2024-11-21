import pandas as pd
import os
from datetime import datetime, timedelta

# Tanggal default (bisa diganti saat diimpor)
TODAY_DATE = datetime(2024, 11, 16)

# Default folder (bisa diganti saat diimpor)
DATA_FOLDER = 'dags/hasil data extract'
PROCESSED_FOLDER = 'dags/hasil data extract'
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Dictionary untuk mapping jenis produk berdasarkan nama file
JENIS_PRODUK_MAPPING = {
    "FemaleDaily_Review Azarine Calm My Acne Sunscreen Moisturizer.csv": "Azarine Calm My Acne Sunscreen Moisturizer",
    "FemaleDaily_Review Azarine Hydramax C Sunscreen Serum.csv": "Azarine Hydramax C Sunscreen Serum",
    "FemaleDaily_Review Azarine Hydrashoote Sunscreen Gel.csv": "Azarine Hydrashoote Sunscreen Gel",
    "FemaleDaily_Review Skinaqua UV Moisture Gel.csv": "Skinaqua UV Moisture Gel",
    "FemaleDaily_Review Skinaqua UV Moisture Milk.csv": "Skinaqua UV Moisture Milk",
    "FemaleDaily_Review Skinaqua UV Whitening Milk.csv": "Skinaqua UV Whitening Milk",
}

# Fungsi untuk mengonversi tanggal
def convert_date(date_str, today_date=datetime.today(), default_date=None):
    try:
        # Cek jika date_str adalah NaN
        if pd.isna(date_str) or date_str == 'NaN':  # Check if the date is NaN
            return default_date or today_date.strftime("%Y-%m-%d")  # Gunakan default_date atau today_date
        
        # Pisahkan jika ada koma (",")
        if ',' in date_str:
            parts = date_str.split(',')
            relative_part = parts[0].strip()
            explicit_date_part = parts[1].strip()
            
            # Parsing waktu relatif (misal "2 days ago")
            if "day" in relative_part:
                days = int(relative_part.split()[0]) if "an" not in relative_part else 1
                relative_date = today_date - timedelta(days=days)
            elif "hour" in relative_part:
                hours = int(relative_part.split()[0]) if "an" not in relative_part else 1
                relative_date = today_date - timedelta(hours=hours)
            else:
                relative_date = today_date
            
            # Parsing tanggal eksplisit (misal "08 Nov 2024")
            try:
                explicit_date = datetime.strptime(explicit_date_part, "%d %b %Y")
            except ValueError:
                explicit_date = None
            
            # Ambil yang lebih spesifik (prioritas waktu relatif)
            return relative_date.strftime("%Y-%m-%d") if relative_date < explicit_date else explicit_date.strftime("%Y-%m-%d")
        
        # Jika hanya format standar (misal "2024-11-20")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            pass  # Lanjutkan ke format lain

        # Jika hanya waktu relatif
        if "hour" in date_str:
            hours = int(date_str.split()[0]) if "an" not in date_str else 1
            return (today_date - timedelta(hours=hours)).strftime("%Y-%m-%d")
        elif date_str == "a day ago":
            return (today_date - timedelta(days=1)).strftime("%Y-%m-%d")
        elif "days ago" in date_str:
            days = int(date_str.split()[0])
            return (today_date - timedelta(days=days)).strftime("%Y-%m-%d")
        elif "months ago" in date_str:
            months = int(date_str.split()[0])
            return (today_date - timedelta(days=30 * months)).strftime("%Y-%m-%d")
        elif "years ago" in date_str:
            years = int(date_str.split()[0])
            return (today_date - timedelta(days=365 * years)).strftime("%Y-%m-%d")
        else:
            return datetime.strptime(date_str, "%d %b %Y").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error memproses tanggal: {date_str} - {e}")
        return default_date or today_date.strftime("%Y-%m-%d")  # Gunakan default_date atau today_date

# Fungsi 1: Proses data dan tambahkan kolom
def process_data(data_folder=DATA_FOLDER, processed_folder=PROCESSED_FOLDER, jenis_produk_mapping=JENIS_PRODUK_MAPPING):
    os.makedirs(processed_folder, exist_ok=True)
    for file_name in os.listdir(data_folder):
        if file_name.startswith("FemaleDaily") and file_name.endswith(".csv"):
            print(f"Memproses file: {file_name}")
            file_path = os.path.join(data_folder, file_name)
            
            df = pd.read_csv(file_path)
            if file_name in jenis_produk_mapping:
                jenis_produk = jenis_produk_mapping[file_name]
                df['jenis_produk'] = jenis_produk
            else:
                print(f"Tidak ada mapping untuk file: {file_name}")
                df['jenis_produk'] = "Unknown"
            
            if 'date' in df.columns:
                df['date'] = df['date'].apply(lambda x: convert_date(x))
            else:
                print(f"Tidak ada kolom 'date' di file {file_name}")
            
            output_path = os.path.join(processed_folder, file_name)
            df.to_csv(output_path, index=False)
            print(f"Hasil diproses disimpan di: {output_path}")

# Fungsi 2: Gabungkan file berdasarkan grup
def merge_files(group_mapping, processed_folder=PROCESSED_FOLDER):
    for group_name, file_list in group_mapping.items():
        dfs = []
        for file_name in file_list:
            file_path = os.path.join(processed_folder, file_name)
            if os.path.exists(file_path):
                print(f"Membaca file: {file_name}")
                df = pd.read_csv(file_path)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]  # Drop kolom 'Unnamed' jika ada
                dfs.append(df)
            else:
                print(f"File tidak ditemukan: {file_name}")
        
        if dfs:
            merged_df = pd.concat(dfs, ignore_index=True)
            output_file = os.path.join(processed_folder, f"FemaleDaily_Sunscreen {group_name}.csv")
            merged_df.to_csv(output_file, index=False)
            print(f"Hasil penggabungan disimpan di: {output_file}")
        else:
            print(f"Tidak ada file yang berhasil digabungkan untuk grup: {group_name}")

def transform_female_daily(**kwargs):
    process_data()
    group_mapping = {
        "Azarine": [
            "FemaleDaily_Review Azarine Calm My Acne Sunscreen Moisturizer.csv",
            "FemaleDaily_Review Azarine Hydramax C Sunscreen Serum.csv",
            "FemaleDaily_Review Azarine Hydrashoote Sunscreen Gel.csv",
        ],
        "Skinaqua": [
            "FemaleDaily_Review Skinaqua UV Moisture Gel.csv",
            "FemaleDaily_Review Skinaqua UV Moisture Milk.csv",
            "FemaleDaily_Review Skinaqua UV Whitening Milk.csv",
        ],
    }
    merge_files(group_mapping)
    
    # Ambil data dari file hasil penggabungan
    processed_folder = "dags/hasil data extract"
    output_file = os.path.join(processed_folder, "FemaleDaily_Sunscreen Azarine.csv")  # Contoh grup Azarine
    df = pd.read_csv(output_file)
    
    # Simpan ke XCom
    ti = kwargs['ti']
    review_data = df.to_dict('records')  # Konversi DataFrame ke list of dictionaries
    ti.xcom_push(key='transformed_data', value=review_data)
    print("Data berhasil disimpan ke XCom.")

if __name__ == "__main__":
    transform_female_daily()
