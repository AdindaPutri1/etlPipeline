from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from etl.extract_google_trends import extract_google_trends
from etl.transform_female_daily import transform_female_daily
from etl.load import insert_data_to_postgres
from etl.transform_google_trends import process_all_files
from etl.transform_merge_data import merge
from etl.transform_cleaning import clean

# Konfigurasi default untuk DAG
default_args = {
    "start_date": datetime(2024, 11, 20),
    "catchup": False,
}

with DAG(
    dag_id="etl_pipeline",
    default_args=default_args,
    schedule_interval="@daily",
    description="DAG untuk ETL modular",
) as dag:


    # Task untuk Transformasi Female Daily
    task_extract_google_trends = PythonOperator(
        task_id="extract_google_trends",
        python_callable=extract_google_trends,
    )

    # Task untuk Transformasi Female Daily
    task_transform_female_daily = PythonOperator(
        task_id="transform_female_daily",
        python_callable=transform_female_daily,
    )

    # Task untuk Transformasi Female Daily
    task_transform_google_trends = PythonOperator(
        task_id="transform_google_trends",
        python_callable=process_all_files,
    )

    # Task untuk Transformasi Female Daily
    task_transform_merge_data = PythonOperator(
        task_id="transform_merge_data",
        python_callable=merge,
    )

    # Task untuk Transformasi Female Daily
    task_transform_cleaning = PythonOperator(
        task_id="transform_cleaning",
        python_callable=clean,
    )

    # Task untuk Membuat Tabel Azarine di PostgreSQL
    create_table_azarine = PostgresOperator(
        task_id='create_table_azarine',
        postgres_conn_id='skincare_connection',
        sql="""
        CREATE TABLE IF NOT EXISTS sunscreen_azarine (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            date TIMESTAMP,
            review_content TEXT,
            purchase_point TEXT,
            recommend TEXT,
            rating INTEGER,
            jenis_produk TEXT,
            trend INTEGER,
            age_category TEXT,
            periode_penggunaan TEXT,
            skintype TEXT,
            skintone TEXT,
            undertone TEXT
        );
    """,
)

# Task untuk Membuat Tabel Skinaqua di PostgreSQL
    create_table_skinaqua = PostgresOperator(
        task_id='create_table_skinaqua',
        postgres_conn_id='skincare_connection',
        sql="""
        CREATE TABLE IF NOT EXISTS sunscreen_skinaqua (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            date TIMESTAMP,
            review_content TEXT,
            purchase_point TEXT,
            recommend TEXT,
            rating INTEGER,
            jenis_produk TEXT,
            trend INTEGER,
            age_category TEXT,
            periode_penggunaan TEXT,
            skintype TEXT,
            skintone TEXT,
            undertone TEXT
        );
    """,
)

    # Task untuk Memasukkan Data ke PostgreSQL
    task_load_to_postgres = PythonOperator(
        task_id="insert_data_to_postgres",
        python_callable=insert_data_to_postgres,
        provide_context=True,
    )

    # Definisi alur antar task
    task_extract_google_trends >> task_transform_female_daily >> task_transform_google_trends >> task_transform_merge_data >> task_transform_cleaning >> create_table_azarine >> create_table_skinaqua >> task_load_to_postgres
