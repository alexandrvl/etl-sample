import os
import pandas as pd
import duckdb
import subprocess
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the data directory
data_dir = 'dbt/data'
parquet_dir = f'{data_dir}/parquet'
duckdb_path = f'{data_dir}/analytics.duckdb'

def extract_postgres_to_parquet():
    print("Starting data extraction...")
    # Ensure directories exist
    os.makedirs(parquet_dir, exist_ok=True)

    # Define tables to extract
    tables = ['customers', 'orders', 'order_items']

    # Get PostgreSQL credentials from environment variables
    pg_user = os.getenv('POSTGRES_USER')
    pg_password = os.getenv('POSTGRES_PASSWORD')
    pg_host = os.getenv('POSTGRES_HOST')
    pg_port = os.getenv('POSTGRES_PORT')
    pg_db = os.getenv('POSTGRES_DB')

    # PostgreSQL connection string
    postgres_conn = f'postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}'

    # Connect to DuckDB
    conn = duckdb.connect(duckdb_path)

    # Install and load PostgreSQL extension if not already loaded
    conn.execute("INSTALL postgres_scanner; LOAD postgres_scanner;")

    for table in tables:
        print(f"Extracting {table} from Postgres...")
        # Extract data from PostgreSQL directly to Parquet using DuckDB
        parquet_file = f'{parquet_dir}/{table}.parquet'
        conn.execute(f"""
            COPY (
                SELECT * FROM postgres_scan(
                    '{postgres_conn}', 
                    'public',
                    'SELECT * FROM {table}'
                )
            ) TO '{parquet_file}' (FORMAT PARQUET)
        """)
        print(f"Saved {table} to {parquet_file}")

    conn.close()
    return "Data extraction completed successfully"

def load_parquet_to_duckdb():
    # Connect to DuckDB
    conn = duckdb.connect(duckdb_path)

    # Define tables to load
    tables = ['customers', 'orders', 'order_items']

    # Create a schema for raw data
    conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

    for table in tables:
        parquet_file = f'{parquet_dir}/{table}.parquet'
        print(f"Loading {parquet_file} into DuckDB...")

        # Create table in raw schema and load data
        conn.execute(f"""
            CREATE OR REPLACE TABLE raw.{table} AS 
            SELECT * FROM read_parquet('{parquet_file}')
        """)

        print(f"Loaded {table} into DuckDB raw schema")

    # Verify data is loaded by counting records in each table
    for table in tables:
        result = conn.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()
        print(f"Table raw.{table} has {result[0]} records")

    conn.close()
    return "Data loaded into DuckDB successfully"


def run_dbt_models():
    print("Running dbt models...")
    # Change to the dbt project directory
    dbt_project_dir = './dbt'  # Changed from '{data_dir}/dbt'

    # Set profiles directory to project root where profiles.yml is located
    profiles_dir = '.'  # Changed from dbt_project_dir

    # Run dbt command with correct paths
    cmd = f'cd {dbt_project_dir} && DBT_PROFILES_DIR={profiles_dir} dbt run --no-use-colors'

    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return "DBT models run successfully"
    except subprocess.CalledProcessError as e:
        print(f"Error running dbt models: {e}")
        print(e.stdout)
        print(e.stderr)
        raise

def export_dbt_models_to_parquet():
    # Ensure directories exist
    dbt_parquet_dir = f'{parquet_dir}/dbt_models'
    os.makedirs(dbt_parquet_dir, exist_ok=True)

    # Connect to DuckDB
    conn = duckdb.connect(duckdb_path)

    # Define dbt models to export
    dbt_models = ['customer_orders', 'order_details']

    # Get list of all tables in DuckDB
    tables_query = """
        SELECT table_name, table_schema 
        FROM information_schema.tables 
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
    """
    available_tables = conn.execute(tables_query).fetchdf()
    print(f"Available tables in DuckDB: {available_tables}")

    for model in dbt_models:
        try:
            print(f"Exporting {model} from DuckDB to Parquet...")

            # Use DuckDB's COPY command to export directly to Parquet
            parquet_file = f'{dbt_parquet_dir}/{model}.parquet'

            # Try with and without schema prefix
            try:
                # First try with main schema (default dbt output schema)
                conn.execute(f"""
                    COPY (SELECT * FROM main.{model}) 
                    TO '{parquet_file}' (FORMAT PARQUET)
                """)
                print(f"Exported {model} from main schema to {parquet_file}")
            except Exception as schema_error:
                try:
                    # Then try without schema prefix
                    conn.execute(f"""
                        COPY (SELECT * FROM {model}) 
                        TO '{parquet_file}' (FORMAT PARQUET)
                    """)
                    print(f"Exported {model} from default schema to {parquet_file}")
                except Exception as no_schema_error:
                    print(f"Warning: Model {model} does not exist in DuckDB. Skipping export.")
                    print(f"Error details: {str(schema_error)}, {str(no_schema_error)}")
                    continue

        except Exception as e:
            print(f"Error exporting {model}: {str(e)}")
            raise

    conn.close()
    return "DBT model export completed successfully"

def main():
    print(f"Starting pipeline run at {datetime.now()}")

    try:
        # Step 1: Extract data from Postgres and save as Parquet
        print("\n=== STEP 1: Extract data from Postgres ===")
        extract_result = extract_postgres_to_parquet()
        print(extract_result)

        # Step 2: Load Parquet data into DuckDB
        print("\n=== STEP 2: Load data into DuckDB ===")
        load_result = load_parquet_to_duckdb()
        print(load_result)

        # Step 3: Run dbt models
        print("\n=== STEP 3: Run dbt models ===")
        dbt_result = run_dbt_models()
        print(dbt_result)

        # Step 4: Export dbt model outputs to Parquet
        print("\n=== STEP 4: Export dbt models to Parquet ===")
        export_result = export_dbt_models_to_parquet()
        print(export_result)

        print(f"\nPipeline completed successfully at {datetime.now()}")
    except Exception as e:
        print(f"\nPipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()
