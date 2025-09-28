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

-- Table des rôles
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL
);

-- Table des participants
CREATE TABLE IF NOT EXISTS participants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    profession VARCHAR(255),
    password VARCHAR(255),
    role_id INT REFERENCES roles(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table des sessions
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    heure_debut TIMESTAMP NOT NULL,
    heure_fin TIMESTAMP NOT NULL,
    conferenciers VARCHAR(255),
    salle VARCHAR(100)
);

-- Table des questions
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'non_repondu',
    session_id INT REFERENCES sessions(id),
    participant_id INT REFERENCES participants(id)
);

-- Insertion des rôles de base
INSERT INTO roles (nom) VALUES ('participant')
    ON CONFLICT (nom) DO NOTHING;
INSERT INTO roles (nom) VALUES ('moderateur')
    ON CONFLICT (nom) DO NOTHING;
INSERT INTO roles (nom) VALUES ('admin')
    ON CONFLICT (nom) DO NOTHING;
