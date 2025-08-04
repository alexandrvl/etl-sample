# ETL Sample Project

This repository contains a sample ETL (Extract, Transform, Load) pipeline that demonstrates how to:
1. Extract data from a PostgreSQL database
2. Transform it using dbt (data build tool)
3. Load it into DuckDB for analytics
4. Export the transformed data as Parquet files

## Project Overview

This project implements a simple ETL pipeline for an e-commerce dataset with customers, orders, and order items. The pipeline:

- Uses Docker to set up a PostgreSQL database with sample data
- Extracts data from PostgreSQL and saves it as Parquet files
- Loads the Parquet files into DuckDB
- Transforms the data using dbt models
- Exports the transformed data back to Parquet files

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git

## Setup Instructions

1. Clone this repository:
   ```
   git clone <repository-url>
   cd etl-sample
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Create a `.env` file from the sample:
   ```
   cp sample-.env .env
   ```

4. Start the PostgreSQL database using Docker:
   ```
   docker-compose up -d
   ```

5. Wait for the database to initialize with sample data (this may take a few seconds).

## Running the Pipeline

Execute the ETL pipeline with:

```
python run_pipeline.py
```

This will:
1. Extract data from PostgreSQL to Parquet files
2. Load the Parquet files into DuckDB
3. Run dbt models to transform the data
4. Export the transformed data to Parquet files

## Project Structure

```
etl-sample/
├── dbt/                        # dbt project directory
│   ├── models/                 # dbt models
│   │   ├── marts/              # Analytics-ready models
│   │   │   ├── customer_orders.sql
│   │   │   └── order_details.sql
│   │   └── staging/            # Staging models
│   │       ├── stg_customers.sql
│   │       ├── stg_order_items.sql
│   │       └── stg_orders.sql
│   ├── dbt_project.yml         # dbt project configuration
│   └── profiles.yml            # dbt connection profiles
├── init-scripts/               # Database initialization scripts
│   └── 01-init-sample-db.sql   # Creates tables and sample data
├── docker-compose.yml          # Docker configuration
├── requirements.txt            # Python dependencies
├── run_pipeline.py             # Main ETL script
├── sample-.env                 # Sample environment variables
└── README.md                   # This file
```

## Data Model

The project uses a simple e-commerce data model:

- **Customers**: Information about customers
- **Orders**: Orders placed by customers
- **Order Items**: Individual items within each order

The dbt models transform this data into:

- **customer_orders**: Aggregated customer metrics (order count, total spent, etc.)
- **order_details**: Detailed view of orders with customer and item information

## Environment Variables

Configure the following environment variables in your `.env` file:

- `POSTGRES_USER`: PostgreSQL username (default: postgres)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: postgres)
- `POSTGRES_DB`: PostgreSQL database name (default: sample_db)
- `POSTGRES_HOST`: PostgreSQL host (default: localhost)
- `POSTGRES_PORT`: PostgreSQL port (default: 5433)

## Output

After running the pipeline, you'll find:

- Raw data in `dbt/data/parquet/`
- Transformed data in `dbt/data/parquet/dbt_models/`
- DuckDB database at `dbt/data/analytics.duckdb`

## License

This project is licensed under the terms of the LICENSE file included in this repository.