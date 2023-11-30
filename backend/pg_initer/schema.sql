CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.nodes (
    id UUID PRIMARY KEY,
    osm_id BIGINT,
    title TEXT,
    role TEXT,
    station_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.railway_nodes (
    id UUID PRIMARY KEY,
    node_osm_id BIGINT,
    railway_osm_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.railway_way (
    id UUID PRIMARY KEY,
    way_osm_id BIGINT,
    railway_osm_id BIGINT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.ways (
    id UUID PRIMARY KEY,
    osm_id BIGINT,
    length INTEGER,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.railways (
    id UUID PRIMARY KEY,
    osm_id BIGINT,
    title TEXT,
    title_from TEXT,
    title_to TEXT,
    operator TEXT,
    network TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.wagons (
    id UUID PRIMARY KEY,
    train_id UUID,
    number INTEGER,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.trains (
    id UUID PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);