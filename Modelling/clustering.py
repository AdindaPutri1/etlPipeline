# -*- coding: utf-8 -*-
"""Untitled15.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19xNXTjJ9UHLaiSFqjYkqjbt6PZEzkD-Q
"""

from google.colab import drive
drive.mount('/content/drive')

import pandas as pd

# Path ke file di Google Drive
skin_aqua_path = '/content/drive/My Drive/dataETL/Clean_Sunscreen Skinaqua.csv'
azarine_path = '/content/drive/My Drive/dataETL/Clean_Sunscreen Azarine.csv'

# Baca file CSV
skin_aqua = pd.read_csv(skin_aqua_path)
azarine = pd.read_csv(azarine_path)

# Gabungkan file
merged_data = pd.concat([skin_aqua, azarine], ignore_index=True)

# Simpan hasil ke Google Drive
output_path = '/content/drive/My Drive/dataETL/Merged_Sunscreen_Data.csv'
merged_data.to_csv(output_path, index=False)

print(f"File berhasil digabungkan dan disimpan di: {output_path}")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.cluster import KMeans

file_path = "/content/drive/My Drive/dataETL/Merged_Sunscreen_Data.csv"
data = pd.read_csv(file_path)

# Pilih kolom yang relevan
columns_of_interest = ['skintype', 'Jenis_Produk', 'trend', 'age_category', 'periode_penggunaan']

# Periksa apakah kolom tersedia
missing_columns = [col for col in columns_of_interest if col not in data.columns]
if missing_columns:
    raise ValueError(f"Kolom berikut tidak ditemukan dalam dataset: {missing_columns}")

# Pilih subset data
data_subset = data[columns_of_interest].copy()

from sklearn.preprocessing import OneHotEncoder, StandardScaler

# One-hot encoding untuk kolom kategorikal
categorical_columns = ['skintype', 'Jenis_Produk', 'age_category', 'periode_penggunaan']
one_hot_encoder = OneHotEncoder(sparse_output=False, drop='first')  # Gunakan sparse_output=False
encoded_categorical = one_hot_encoder.fit_transform(data_subset[categorical_columns])

# Konversi hasil encoding ke DataFrame
encoded_categorical_df = pd.DataFrame(
    encoded_categorical,
    columns=one_hot_encoder.get_feature_names_out(categorical_columns)
)

# Gabungkan data numerik (misalnya, trend)
numerical_columns = ['trend']
final_data = pd.concat([encoded_categorical_df, data_subset[numerical_columns].reset_index(drop=True)], axis=1)

"""Normalisasi data"""

scaler = StandardScaler()
scaled_data = scaler.fit_transform(final_data)

"""Tentukan jumlah cluster optimal menggunakan Elbow Method"""

sse = []
k_range = range(1, 11)
for k in k_range:
    kmeans = KMeans(n_clusters=k, random_state=42)
    kmeans.fit(scaled_data)
    sse.append(kmeans.inertia_)

"""**Plot Elbow Method**"""

plt.figure(figsize=(8, 5))
plt.plot(k_range, sse, marker='o')
plt.title('Elbow Method untuk Menentukan Jumlah Cluster Optimal')
plt.xlabel('Jumlah Cluster (k)')
plt.ylabel('Sum of Squared Errors (SSE)')
plt.show()

"""Jika Anda ingin fokus pada interpretasi lebih sederhana, gunakan 3 cluster.

Jika data kompleksitasnya tinggi dan membutuhkan pengelompokan lebih terperinci, gunakan 4 cluster.
"""

# berdasarkan elbow method
optimal_clusters = 4

# Clustering dengan jumlah cluster optimal
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
data_subset['cluster'] = kmeans.fit_predict(scaled_data)

# Analisis hasil clustering
cluster_analysis = data_subset.groupby('cluster').size()

distribution = encoded_categorical_df.sum().sort_values(ascending=False)

# Simpan hasil distribusi fitur One-Hot Encoding ke dalam file CSV
distribution_file_path = 'distribution_one_hot_encoding.csv'
distribution.to_csv(distribution_file_path, header=True)

# Visualisasi distribusi fitur hasil encoding
plt.figure(figsize=(10, 8))
distribution.plot(kind='barh')
plt.title("Distribusi Fitur Hasil One-Hot Encoding")
plt.xlabel("Jumlah (Count)")
plt.ylabel("Fitur")
plt.show()

"""Fitur age_category_dewasa muda memiliki jumlah kemunculan tertinggi, menunjukkan bahwa mayoritas data dalam dataset berasal dari kategori usia dewasa muda.

Fitur Jenis_Produk_Azarine Hydrashooté Sunscreen Gel dan periode_penggunaan_Jangka Pendek juga memiliki jumlah kemunculan yang cukup tinggi, menunjukkan preferensi terhadap produk tersebut atau pola penggunaan jangka pendek.

Fitur seperti skintype_nan dan age_category_paruh baya memiliki jumlah kemunculan yang sangat rendah, menunjukkan bahwa data untuk kategori ini jarang muncul atau hampir tidak ada.
"""

# Visualisasi hasil clustering
plt.figure(figsize=(8, 5))
sns.countplot(data=data_subset, x='cluster', palette='viridis')
plt.title('Distribusi Cluster')
plt.xlabel('Cluster')
plt.ylabel('Jumlah Data')
plt.show()

# Simpan hasil clustering ke file
output_file_path = 'clustering_results.csv'
data_subset.to_csv(output_file_path, index=False)
print(f"Hasil clustering disimpan di {output_file_path}")

skin_features = data[['skintype']]

# Fitur kategori usia
age_features = data[['age_category']]

# Fitur jenis produk
product_features = data[['Jenis_Produk']]

period_features = data[['periode_penggunaan']]

# 2. Terapkan One-Hot Encoding untuk setiap subset fitur
encoder = OneHotEncoder(sparse_output=False, drop='first')

# Encode tipe kulit
encoded_skin = encoder.fit_transform(skin_features)
encoded_skin_df = pd.DataFrame(encoded_skin, columns=encoder.get_feature_names_out(['skintype']))

# Encode kategori usia
encoded_age = encoder.fit_transform(age_features)
encoded_age_df = pd.DataFrame(encoded_age, columns=encoder.get_feature_names_out(['age_category']))

# Encode jenis produk
encoded_product = encoder.fit_transform(product_features)
encoded_product_df = pd.DataFrame(encoded_product, columns=encoder.get_feature_names_out(['Jenis_Produk']))

# Encode periode penggunaan
encoded_period = encoder.fit_transform(period_features)
encoded_period_df = pd.DataFrame(encoded_period, columns=encoder.get_feature_names_out(['periode_penggunaan']))

# 3. Clustering untuk setiap subset
def cluster_and_plot(data_subset, n_clusters=3, title="Clustering Results"):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_subset)

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)

    # Tambahkan hasil cluster ke data
    data_subset['cluster'] = clusters

     # Visualisasi cluster
    plt.figure(figsize=(8, 5))  # Perhatikan indentasi ini
    sns.countplot(x='cluster', data=data_subset, palette='viridis')
    plt.title(title)
    plt.xlabel('Cluster')
    plt.ylabel('Jumlah Data')
    plt.show()

    return data_subset

# Clustering tipe kulit
clustered_skin = cluster_and_plot(encoded_skin_df, n_clusters=3, title="Clustering for Skin Type")

# Clustering kategori usia
clustered_age = cluster_and_plot(encoded_age_df, n_clusters=3, title="Clustering for Age Category")

# Clustering jenis produk
clustered_product = cluster_and_plot(encoded_product_df, n_clusters=3, title="Clustering for Product Type")

# Clustering periode penggunaan
clustered_period = cluster_and_plot(encoded_period_df, n_clusters=3, title="Clustering for Usage Period")

# Simpan ke CSV
clustered_skin.to_csv('clustering_skin.csv', index=False)
clustered_age.to_csv('clustering_age.csv', index=False)
clustered_product.to_csv('clustering_product.csv', index=False)
clustered_period.to_csv('clustering_period.csv', index=False)

print("Hasil clustering telah disimpan sebagai CSV.")

"""Menambahkan clustering ke data merge"""

# 3. Clustering untuk setiap subset
def apply_clustering(data_subset, n_clusters=3):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data_subset)

    # KMeans clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    return clusters

# Tambahkan hasil clustering ke data asli
data['cluster_skin'] = apply_clustering(encoded_skin_df, n_clusters=4)
data['cluster_age'] = apply_clustering(encoded_age_df, n_clusters=4)
data['cluster_product'] = apply_clustering(encoded_product_df, n_clusters=4)
data['cluster_period'] = apply_clustering(encoded_period_df, n_clusters=4)

# 4. Simpan hasil data dengan clustering ke file CSV
output_file_path = 'merged_dataClustering_Sunscreen.csv'
data.to_csv(output_file_path, index=False)

print(f"Hasil data dengan clustering telah disimpan sebagai '{output_file_path}'.")

# Simpan hasil ke Google Drive
output_path = '/content/drive/My Drive/dataETL/Merged_SunscreenDataClustering.csv'
merged_data.to_csv(output_path, index=False)

print(f"File berhasil digabungkan dan disimpan di: {output_path}")

# Visualisasi distribusi hasil clustering langsung dari data gabungan
import matplotlib.pyplot as plt
import seaborn as sns

# Visualisasi distribusi untuk masing-masing cluster
clusters = ['cluster_skin', 'cluster_age', 'cluster_product', 'cluster_period']
titles = [
    'Distribusi Cluster Berdasarkan Skin Type',
    'Distribusi Cluster Berdasarkan Age Category',
    'Distribusi Cluster Berdasarkan Product Type',
    'Distribusi Cluster Berdasarkan Usage Period'
]

# Loop untuk visualisasi semua cluster
for cluster, title in zip(clusters, titles):
    plt.figure(figsize=(8, 6))
    sns.countplot(x=cluster, data=data, palette='viridis')
    plt.title(title)
    plt.xlabel('Cluster')
    plt.ylabel('Jumlah Data')
    plt.show()

# Analisis karakteristik cluster
clusters = ['cluster_skin', 'cluster_age', 'cluster_product', 'cluster_period']

for cluster in clusters:
    print(f"\n--- Analisis untuk {cluster} ---")

    # Distribusi fitur kategorikal
    for col in ['skintype', 'age_category', 'Jenis_Produk', 'period']:
        if col in data.columns:
            print(f"\nDistribusi {col} untuk {cluster}:")
            print(data.groupby(cluster)[col].value_counts(normalize=True))

    # Rata-rata fitur numerik
    print("\nRata-rata fitur numerik:")
    print(data.groupby(cluster)[['trend', 'rating']].mean())

"""Kesimpulan Umum
Cluster Skin:
Cluster 0-3 jelas membagi pengguna berdasarkan tipe kulit (Dry, Combination, Normal, Oily).
Setiap cluster menunjukkan produk yang lebih cocok untuk tipe kulit tertentu.

Cluster Age:
Cluster berdasarkan usia memisahkan pengguna dengan preferensi berbeda berdasarkan kategori umur.

Cluster Product:
Cluster ini menunjukkan dominasi preferensi untuk produk tertentu, seperti Skinaqua UV Whitening Milk untuk Cluster 0.

Cluster Period:
Distribusi periode penggunaan menunjukkan bahwa Azarine Hydrashoote Sunscreen Gel populer di semua cluster.

# **Cluster Skin**

Distribusi Skin Type
Cluster 0: Dominasi Dry (100%).
Cluster 1: Dominasi Combination (100%).
Cluster 2: Dominasi Normal (100%).
Cluster 3: Dominasi Oily (100%).

Distribusi Age Category
Cluster 0:
Dewasa Muda mendominasi (78.26%), disusul Dewasa Matang (19.57%).

Cluster 1:
Didominasi oleh Dewasa Muda (66.90%), tetapi Remaja memiliki proporsi yang lebih besar dibandingkan cluster
lainnya (13.38%).

Cluster 2:
Sebagian besar Dewasa Muda (82.22%), dengan Remaja dan Dewasa Matang masing-masing 8.89%.

Cluster 3:
Didominasi oleh Dewasa Muda (83.13%), tetapi memiliki Remaja (9.64%) lebih banyak dibandingkan cluster 2.

Distribusi Jenis Produk
Cluster 0:
Azarine Hydrashoote Sunscreen Gel paling populer (41.30%), diikuti oleh Skinaqua UV Whitening Milk (23.91%).

Cluster 1:
Produk dominan adalah Azarine Hydrashoote Sunscreen Gel (35.21%) dan Skinaqua UV Moisture Milk (19.01%).

Cluster 2:
Dominasi Skinaqua UV Whitening Milk (35.56%) dan Azarine Hydrashoote Sunscreen Gel (26.67%).

Cluster 3:
Azarine Hydrashoote Sunscreen Gel mendominasi (45.78%).

Fitur Numerik (Trend dan Rating)

Trend: Cluster 3 memiliki trend tertinggi (55.63), diikuti cluster 0 (54.20).

Rating: Cluster 1 memiliki rating tertinggi (4.68).

# **Cluster Age**

Distribusi Skin Type

Cluster 0:
Tipe kulit Combination mendominasi (40.08%), disusul oleh Oily (29.11%).

Cluster 1:
Tipe kulit Combination mendominasi penuh (100%).

Cluster 2:
Tipe kulit Combination mendominasi penuh (100%).

Cluster 3:
Didominasi oleh Combination (54.76%) dan Dry (21.43%).

Distribusi Age Category

Cluster 0:
100% pengguna Dewasa Muda.

Cluster 1:
100% pengguna Remaja.

Cluster 2:
100% pengguna Paruh Baya.

Cluster 3:
100% pengguna Dewasa Matang.

Distribusi Jenis Produk

Cluster 0:
Azarine Hydrashoote Sunscreen Gel paling populer (38.82%), diikuti Skinaqua UV Whitening Milk (20.68%).

Cluster 1:
Dominasi Azarine Calm My Acne Sunscreen Moisturizer (25%).

Cluster 2:
Didominasi oleh Azarine Hydrashoote Sunscreen Gel (66.67%).

Cluster 3:
Azarine Hydrashoote Sunscreen Gel (36.36%).

Fitur Numerik (Trend dan Rating)

Trend: Cluster 0 dan 3 memiliki trend tertinggi (53.92).

Rating: Cluster 2 memiliki rating tertinggi (4.67).

# **Cluster Product**

Distribusi Skin Type

Cluster 0:
Didominasi oleh Combination (40.98%) dan Normal (26.23%).

Cluster 1:
Tipe kulit Combination dominan (42.02%), disusul oleh Oily (31.93%).

Cluster 2:
Kombinasi antara Combination (36.36%) dan Normal serta Oily (masing-masing 27.27%).

Cluster 3:
Didominasi oleh Combination (49.59%) dan Oily (26.83%).

Distribusi Age Category

Cluster 0:
Mayoritas pengguna Dewasa Muda (79.03%).

Cluster 1:
Sebagian besar pengguna Dewasa Muda (77.31%).

Cluster 2:
Pengguna Remaja cukup besar (25%), dengan mayoritas tetap Dewasa Muda (58.33%).

Cluster 3:
Mayoritas Dewasa Muda (72.36%).

Distribusi Jenis Produk

Cluster 0:
Dominasi penuh oleh Skinaqua UV Whitening Milk (100%).

Cluster 1:
Dominasi penuh oleh Azarine Hydrashoote Sunscreen Gel (100%).

Cluster 2:
Dominasi penuh oleh Skinaqua UV Moisture Gel (100%).

Cluster 3:
Kombinasi Skinaqua UV Moisture Milk (43.90%) dan Azarine Calm My Acne Sunscreen Moisturizer (35.77%).

Fitur Numerik (Trend dan Rating)

Trend: Cluster 1 memiliki trend tertinggi (54.93).

Rating: Cluster 0 memiliki rating tertinggi (4.77).

# **Cluster Period**

Distribusi Skin Type

Cluster 0:
Didominasi oleh Combination (50.43%) dan Oily (23.48%).

Cluster 1:
Kombinasi Combination (42%) dan Oily (30%).

Cluster 2:
Dominasi Combination (40.40%) dan Oily (26.26%).

Distribusi Age Category

Cluster 0:
Mayoritas pengguna Dewasa Muda (71.79%).

Cluster 1:
Sebagian besar pengguna Dewasa Muda (75%).

Cluster 2:
Sebagian besar pengguna Dewasa Muda (78.79%).

Distribusi Jenis Produk

Cluster 0:
Dominasi Azarine Hydrashoote Sunscreen Gel (41.03%).

Cluster 1:
Azarine Hydrashoote Sunscreen Gel dominan (40%).

Cluster 2:
Azarine Hydrashoote Sunscreen Gel (31.31%) dan Skinaqua UV Whitening Milk (27.27%).

Fitur Numerik (Trend dan Rating)

Trend: Cluster 0 memiliki trend tertinggi (53.70).

Rating: Cluster 2 memiliki rating tertinggi (4.91).
"""
