import os
import psycopg2
from unittest.mock import patch, MagicMock

ENVIRONMENT = os.getenv('DATABASE_URL')


def get_database_connection():
    if ENVIRONMENT is None:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        return mock_conn, mock_cursor
    else:
        conn = psycopg2.connect(ENVIRONMENT)
        cursor = conn.cursor()
        return conn, cursor


def insert_data_to_database(metrics):
    conn, cursor = get_database_connection()
    insert_query = """
    INSERT INTO metrics (session_id, metric_type, value, timestamp)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.executemany(insert_query, metrics)
    if not isinstance(cursor, MagicMock):
        conn.commit()

    cursor.close()
    conn.close()
    print('completed')


def process_stream(data_stream):
    metrics = [(m['session_id'], m['metric_type'], m['value'], m['timestamp']) for m in data_stream]
    insert_data_to_database(metrics)


# Example usage
metrics_data = [
    {
        'session_id': '123e4567-e89b-12d3-a456-426614174000',
        'metric_type': 'talked_time',
        'value': 300,
        'timestamp': '2024-08-13T12:00:00Z'
    },
    {
        'session_id': '123e4567-e89b-12d3-a456-426614174000',
        'metric_type': 'microphone_used',
        'value': 1,
        'timestamp': '2024-08-13T12:05:00Z'
    }
]

process_stream(metrics_data)

