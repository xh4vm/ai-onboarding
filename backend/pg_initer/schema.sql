CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.users (
    id UUID PRIMARY KEY,
    email TEXT,
    password TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);