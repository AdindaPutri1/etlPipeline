# # Menggunakan image Airflow sebagai base image
# FROM apache/airflow:2.10.3-python3.9

# # Salin file requirements
# COPY requirements.txt /requirements.txt

# # Instal dependensi menggunakan pip tanpa opsi --user
# RUN pip install --upgrade pip && pip install --no-cache-dir -r /requirements.txt

# # Jalankan sebagai root untuk mengubah kepemilikan file
# USER root

# # Salin file DAG ke dalam direktori Airflow
# COPY dags /opt/airflow/dags

# # Ubah kepemilikan file agar user airflow memiliki akses
# RUN chown -R airflow: /opt/airflow/dags

# # Kembali ke user airflow untuk menjalankan proses Airflow
# USER airflow

# # Entrypoint bawaan Airflow
# ENTRYPOINT ["/usr/bin/dumb-init", "--"]

# # Default menjalankan webserver
# CMD ["webserver"]