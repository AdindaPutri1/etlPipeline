from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime
from etl.extract_google_trends import extract_google_trends
from etl.transform_female_daily import transform_female_daily
from etl.load import insert_female_daily_data_into_postgres
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

    # Task untuk Membuat Tabel di PostgreSQL
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='skincare_connection',
        sql="""
        CREATE TABLE IF NOT EXISTS female_daily_reviews (
            id SERIAL PRIMARY KEY,
            username TEXT NOT NULL,
            age TEXT,
            profile_description TEXT,
            date TEXT,
            review_content TEXT,
            usage_period TEXT,
            purchase_point TEXT,
            recommend TEXT,
            rating_count DECIMAL,
            jenis_produk TEXT
);
        """,
    )

    # Task untuk Memasukkan Data ke PostgreSQL
    task_load_to_postgres = PythonOperator(
        task_id="load_to_postgres",
        python_callable=insert_female_daily_data_into_postgres,
        provide_context=True,
    )

    # Definisi alur antar task
    task_extract_google_trends >> task_transform_female_daily >> task_transform_google_trends >> task_transform_merge_data >> task_transform_cleaning >> create_table >> task_load_to_postgres
