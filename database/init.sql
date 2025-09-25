-- Crée l'utilisateur (seulement si inexistant)
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'congres_user') THEN
        CREATE ROLE congres_user WITH LOGIN PASSWORD 'postgres';
    END IF;
END
$$;

-- Crée la base (seulement si inexistante)
DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'congres_db') THEN
        CREATE DATABASE congres_db OWNER congres_user;
    END IF;
END
$$;

-- Création d'une table minimaliste de test
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'non_repondu'
);
