CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.users (
    id UUID PRIMARY KEY,
    email TEXT,
    password TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.questions (
    id UUID PRIMARY KEY,
    user_id UUID,
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.answers (
    id UUID PRIMARY KEY,
    question_id UUID,
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.viewed_answers (
    id UUID PRIMARY KEY,
    answer_id UUID,
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);