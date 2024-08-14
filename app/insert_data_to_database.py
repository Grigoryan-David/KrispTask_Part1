import os
import psycopg2
from unittest.mock import MagicMock

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
    def insert_metrics(metrics):
        conn, cursor = get_database_connection()
        metric_query = """
        INSERT INTO metrics (session_id, metric_type, value, timestamp)
        VALUES (%s, %s, %s, %s)
        """
        sentiment_query = """
        INSERT INTO voice_sentiment (session_id, sentiment_score, timestamp)
        VALUES (%s, %s, %s)
        """

        metric_data = []
        sentiment_data = []
        for data in metrics:
            if data['metric_type'] == 'voice_sentiment':
                sentiment_data.append((
                    data['session_id'],
                    data['value'],  # sentiment_score
                    data['timestamp']
                ))
            else:
                metric_data.append((
                    data['session_id'],
                    data['metric_type'],
                    data['value'],
                    data['timestamp']
                ))

        if metric_data:
            cursor.executemany(metric_query, metric_data)
        if sentiment_data:
            cursor.executemany(sentiment_query, sentiment_data)
        if not isinstance(cursor, MagicMock):
            conn.commit()
        cursor.close()
        conn.close()


# Example usage
data_stream = [
    {
        'session_id': 'session1',
        'metric_type': 'talked_time',
        'value': 300,
        'timestamp': '2024-08-13T12:00:00Z'
    },
    {
        'session_id': 'session1',
        'metric_type': 'microphone_used',
        'value': 1,
        'timestamp': '2024-08-13T12:05:00Z'
    },
    {
        'session_id': 'session1',
        'metric_type': 'voice_sentiment',
        'value': 0.8,
        'timestamp': '2024-08-13T12:10:00Z'
    }
]
insert_data_to_database(data_stream)


