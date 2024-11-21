import os
import pandas as pd

# Konfigurasi folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = "dags/hasil data transform"
PROCESSED_FOLDER = "dags/hasil data transform"

# Pastikan folder untuk hasil yang telah diproses ada
if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

# Fungsi untuk membaca file CSV
def read_csv_file(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"File tidak ditemukan: {file_path}")
        return None

# Fungsi untuk membersihkan data
def clean_data(df):
    # Buat salinan DataFrame untuk menghindari peringatan
    df = df.copy()

    # Mapping kategori umur
    age_mapping = {
        '18 and Under': 'remaja', 
        '19 - 24': 'dewasa muda',  
        '25 - 29': 'dewasa muda',
        '30 - 34': 'dewasa matang',  
        '35 - 39': 'dewasa matang',
        '40 - 44': 'dewasa matang',
        '45 and Above': 'paruh baya'
    }
    df['age_category'] = df['age'].map(age_mapping)

    # Hapus nilai tidak diinginkan di kolom 'profile_description'
    unwanted_values = [',19 - 24', ',25 - 29', ',18 and Under']
    df = df[~df['profile_description'].isin(unwanted_values)]

    # Mapping periode penggunaan
    usage_period_mapping_id = {
        'Less than 1 week': 'Jangka Pendek',
        '1 week - 1 month': 'Jangka Pendek',
        '1 month - 3 months': 'Jangka Pendek',
        '3 months - 6 months': 'Jangka Menengah',
        '6 months - 1 year': 'Jangka Menengah',
        'More than 1 year': 'Jangka Panjang'
    }
    df['periode_penggunaan'] = df['usage_period'].map(usage_period_mapping_id)

    # Rename kolom
    df = df.rename(columns={'rating_count': 'rating', 'value': 'trend'})

    # Memisahkan kolom 'profile_description'
    split_columns = df['profile_description'].str.split(',', expand=True)
    df['skintype'] = split_columns[0].str.strip()
    df['skintone'] = split_columns[1].str.strip()
    df['undertone'] = split_columns[2].str.strip()

    # Hapus kolom yang tidak diperlukan
    df = df.drop(columns=['usage_period', 'age', 'profile_description'])

    return df

# Fungsi untuk menyimpan DataFrame yang telah dibersihkan
def save_cleaned_data(df, output_file_name):
    output_path = os.path.join(PROCESSED_FOLDER, output_file_name)
    df.to_csv(output_path, index=False)
    print(f"Data telah disimpan di: {output_path}")

# Fungsi untuk memproses file CSV dan membersihkan data
def process_file(input_file_name, output_file_name):
    # Path file input
    input_file_path = os.path.join(DATA_FOLDER, input_file_name)
    
    # Baca file CSV
    df = read_csv_file(input_file_path)
    if df is not None:
        # Bersihkan data
        cleaned_df = clean_data(df)
        
        # Simpan hasil yang sudah dibersihkan
        save_cleaned_data(cleaned_df, output_file_name)

def clean():
    # Nama file input dan output
    input_file_azarine = 'Merged_Sunscreen Azarine.csv'
    output_file_azarine = 'Clean_Sunscreen Azarine.csv'

    input_file_skinaqua = 'Merged_Sunscreen Skinaqua.csv'
    output_file_skinaqua = 'Clean_Sunscreen Skinaqua.csv'

    # Proses file Sunscreen Azarine
    print("Memproses file 'Merged_Sunscreen Azarine.csv'...")
    process_file(input_file_azarine, output_file_azarine)

    # Proses file Sunscreen Skinaqua
    print("Memproses file 'Merged_Sunscreen Skinaqua.csv'...")
    process_file(input_file_skinaqua, output_file_skinaqua)

if __name__ == '__main__':
    clean()
