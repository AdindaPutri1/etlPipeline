from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
import pandas as pd
import logging

def insert_data_to_postgres(**kwargs):
    # Ambil data dari file CSV yang sudah dibersihkan
    input_file_azarine = 'dags/hasil data transform/Clean_Sunscreen Azarine.csv'
    input_file_skinaqua = 'dags/hasil data transform/Clean_Sunscreen Skinaqua.csv'
    
    # Membaca file CSV yang sudah dibersihkan
    skincare_data_azarine = pd.read_csv(input_file_azarine)
    skincare_data_skinaqua = pd.read_csv(input_file_skinaqua)
    
    logging.info("Preview Azarine Data:")
    logging.info(skincare_data_azarine.head())
    logging.info("Azarine Column Names:")
    logging.info(list(skincare_data_azarine.columns))

    logging.info("Preview Skinaqua Data:")
    logging.info(skincare_data_skinaqua.head())
    logging.info("Skinaqua Column Names:")
    logging.info(list(skincare_data_skinaqua.columns))

    # Koneksi ke PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='skincare_connection')
    
    # Query untuk insert data Azarine
    insert_query_azarine = """
    INSERT INTO sunscreen_azarine (
        username, date, review_content, purchase_point, recommend, rating,
        jenis_produk, trend, age_category, periode_penggunaan, 
        skintype, skintone, undertone
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Query untuk insert data Skinaqua
    insert_query_skinaqua = """
    INSERT INTO sunscreen_skinaqua (
        username, date, review_content, purchase_point, recommend, rating, 
        jenis_produk, trend, age_category, periode_penggunaan, 
        skintype, skintone, undertone
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Begin transaction
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    try:
        # Insert data Azarine
        for skincare in skincare_data_azarine.to_dict(orient='records'):
            cursor.execute(insert_query_azarine, (
                skincare['username'],
                skincare['date'],
                skincare['review_content'],
                skincare['purchase_point'],
                skincare['recommend'],
                skincare['rating'],
                skincare['jenis_produk'],
                skincare['trend'],
                skincare['age_category'],
                skincare['periode_penggunaan'],
                skincare['skintype'],
                skincare['skintone'],
                skincare['undertone'],
            ))

        # Insert data Skinaqua
        for skincare in skincare_data_skinaqua.to_dict(orient='records'):
            cursor.execute(insert_query_skinaqua, (
                skincare['username'],
                skincare['date'],
                skincare['review_content'],
                skincare['purchase_point'],
                skincare['recommend'],
                skincare['rating'],
                skincare['jenis_produk'],
                skincare['trend'],
                skincare['age_category'],
                skincare['periode_penggunaan'],
                skincare['skintype'],
                skincare['skintone'],
                skincare['undertone'],
            ))

        conn.commit()
        logging.info("Successfully inserted records into the database.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()
