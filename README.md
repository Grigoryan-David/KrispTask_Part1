# Krisp Project 

## Part 1 Overview
This project is a data ingestion pipeline that processes user metrics, 
such as `talked_time`, `microphone_used`, `speaker_used`, and `voice_sentiment`. 
The pipeline ingests this data into a PostgreSQL database using a Python application, 
all orchestrated with Docker.

## Features
- Processes and stores user metrics.
- Uses PostgreSQL for reliable and scalable data storage.
- Dockerized setup for easy deployment and management.
- Designed for flexibility and future scalability.

## Prerequisites
- Docker and Docker Compose installed on your machine.
- Python 3.12.3.

## Project Structure

krisp/
│
├── app/
│   ├── insert_data_to_database.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── init_db.sql
├── docker-compose.yml
├── README.md



## Setup Instructions

### 1. Clone the Repository:
```bash
git clone https://github.com/Grigoryan-David/KrispTask.git
cd krisp
```

### 2. Build and Start the Containers:
#### Build and start the Docker containers using Docker Compose
```bash
docker-compose up --build
```

### 3. Initialize the Database
#### Access the PostgreSQL container:
```bash
docker exec -it krisp-db-1 psql -U metrics_user -d metrics_db
```
#### Run the init_db.sql script to create the necessary tables:
```sql
\i /var/lib/postgresql/data/init_db.sql
```

### 4. Verify the Setup
#### Ensure the tables were created successfully:
```sql
\dt
\d metrics
```

### 5. Stopping the Containers
#### To stop the running containers, press Ctrl+C or run:
```bash
docker-compose down
```

### Dependencies
#### All required Python packages are listed in requirements.txt. 
#### To install them manually:
```bash
pip install -r app/requirements.txt
```
