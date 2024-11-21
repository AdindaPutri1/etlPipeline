def insert_female_daily_data_into_postgres(**kwargs):
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    import logging
    import pandas as pd

    # Ambil data dari XCom
    ti = kwargs['ti']
    review_data = ti.xcom_pull(key='transformed_data', task_ids='transform_female_daily')
    if not review_data:
        logging.error("Tidak ada data hasil transformasi di XCom.")
        raise ValueError("No transformed data found")

    # Koneksi ke PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id='skincare_connection')
    insert_query = """
    INSERT INTO female_daily_reviews (
        username, age, profile_description, date, review_content,
        usage_period, purchase_point, recommend, rating_count, jenis_produk
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Begin transaction
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    try:
        for review in review_data:
             # Convert NaN to None for date column to be inserted as NULL in PostgreSQL
            if pd.isna(review['date']):
                review['date'] = None

            # Execute insert statement
            cursor.execute(insert_query, (
                review['username'],
                review['age'],
                review['profile_description'],
                review['date'],  # This will be NULL if 'date' is NaN
                review['review_content'],
                review['usage_period'],
                review['purchase_point'],
                review['recommend'],
                review['rating_count'],
                review['jenis_produk'],
            ))
        conn.commit()
        logging.info(f"Successfully inserted {len(review_data)} records into the database.")
    except Exception as e:
        conn.rollback()
        logging.error(f"Error inserting data: {e}")
    finally:
        cursor.close()
        conn.close()
