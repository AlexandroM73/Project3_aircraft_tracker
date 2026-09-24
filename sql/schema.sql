-- Таблица стран
CREATE TABLE IF NOT EXISTS countries (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    bbox_min_lat DOUBLE PRECISION,
    bbox_max_lat DOUBLE PRECISION,
    bbox_min_lon DOUBLE PRECISION,
    bbox_max_lon DOUBLE PRECISION
);

-- Таблица самолётов
CREATE TABLE IF NOT EXISTS aeroplanes (
    icao24 VARCHAR(8) PRIMARY KEY,
    callsign VARCHAR(20),
    origin_country VARCHAR(100),
    time_position DOUBLE PRECISION,
    last_position_time DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    baro_altitude DOUBLE PRECISION,
    velocity DOUBLE PRECISION,
    true_track DOUBLE PRECISION,
    vertical_rate DOUBLE PRECISION,
    on_ground BOOLEAN,
    squawk VARCHAR(4),
    spi BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_aeroplanes_callsign ON aeroplanes(callsign);
