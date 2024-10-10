CREATE DATABASE redpanda;

CREATE TABLE IF NOT EXISTS youtube_video_ids (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255),
    channel_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS wordpress_urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255)
);

