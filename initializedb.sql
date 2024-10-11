CREATE DATABASE feedbeat;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS public.youtube_video_ids (
    id SERIAL PRIMARY KEY,
    video_id VARCHAR(255),
    channel_id VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS public.wordpress_urls (
    id SERIAL PRIMARY KEY,
    url VARCHAR(255)
);

