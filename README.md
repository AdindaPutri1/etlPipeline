# Tugas Rekayasa Data End-to-End Data Engineering
Data Pipeline ETL dengan topik:
**"Azarine vs. Skinaqua:  Mengungkap Tren Preferensi Konsumen Indonesia Terhadap Brand Sunscreen Lokal dan Internasional Menggunakan Clustering Model"**

## _Pipeline Architecture_
![image](https://github.com/user-attachments/assets/0eca93f0-6805-4adb-bc9e-68fe3d48a3ce)

## Member

| No  | Nama                        | NIM                 |
|-----|-----------------------------|---------------------|
| 1   | Fatimah Nadia Eka Putri     | 22/497876/TK/54588  |
| 2   | Adinda Putri Romadhon       | 22/505508/TK/55321  |
| 3   | Tsaniya Khamal Khasanah     | 22/503817/TK/55074  |

## Link Notion Blog Post
https://www.notion.so/End-to-End-Data-Engineering-1436080924fb8078acb2fc862763c5b1?pvs=4

## Link Gdrive Demo
https://drive.google.com/drive/folders/10lOyUo3pMAfyQwT6nLOAulwJYQHKxvqV?usp=sharing

## Prerequisities
1. **Install Docker Desktop**  
   Ensure Docker Desktop is installed and running.  
   [Download Docker Desktop](https://www.docker.com/products/docker-desktop)

2. **Install Python 3.12.3**  
   Ensure Python is installed on your system.  
   [Download Python](https://www.python.org/downloads/)

## Setup Instructions

### Step 1: Create Virtual Environment

1. Open your terminal and navigate to the project directory.
2. Create a virtual environment:
   ```
   python -m venv venv
3. Activate the virtual environment:
   ```
   venv\Scripts\activate

### Step 2: Follow Apache Airflow Docker Setup
1. Go to the [Airflow Docker Compose Setup Guide](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html).
2. Follow the setup steps as per the guide and adjust commands based on your terminal or operating system.

### Step 3: Initialize the Database
    docker compose up airflow-init

### Step 4: Start Airflow
    docker compose up

### Step 5: Chech the DAG
Open http://localhost:8080 to see the dag with the name 'etl_pipeline'

### Step 6: Adjust Code
1. Go to file extract_google_trends and create your own api token at [Apify](https://apify.com/emastra/google-trends-scraper), insert the api token on the requested field
2. This scheduling is set on daily with data for 3 month, adjust the timeRange in file extract_google_trends with today. If you want to get the data for daily, you can add the task for extract_female_daily and adjust the range of the page you want to get and rename the output file. Don't forget to install library dependencies with pip install selenium and pip install beautifulsoup4
3. To see if it's already created on the database, you can login at http://localhost:5050 and enter email and password as you defined in docker-compose.yaml. For this case the email is admin@admin.com and the password is root

### Note:
For troubleshooting, you can check the logs folder to identify what happened or what errors occurred.

