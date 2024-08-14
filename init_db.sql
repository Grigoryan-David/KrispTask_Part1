CREATE TABLE users (
    user_id UUID PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sessions (
    session_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    start_time TIMESTAMPTZ,
    end_time TIMESTAMPTZ,
    device_id VARCHAR(255),
    app_version VARCHAR(50),
    location VARCHAR(255),
    network_quality VARCHAR(50)
);

CREATE TABLE metrics (
    metric_id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id),
    metric_type VARCHAR(50),  -- Can store 'talked_time', 'microphone_used', 'speaker_used'
    value NUMERIC,            -- Stores the actual metric value (e.g., duration, boolean)
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE voice_sentiment (
    sentiment_id SERIAL PRIMARY KEY,
    session_id UUID REFERENCES sessions(session_id),
    sentiment_score NUMERIC,  -- Stores the sentiment score (e.g., a value between -1 and 1)
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_session_id ON metrics(session_id);
CREATE INDEX idx_user_id ON sessions(user_id);
CREATE INDEX idx_timestamp_metrics ON metrics(timestamp);
CREATE INDEX idx_timestamp_sentiment ON voice_sentiment(timestamp);

