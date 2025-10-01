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

-- Table des orateurs (minimal : id + nom)
CREATE TABLE IF NOT EXISTS orateurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(150) NOT NULL
);

-- Table des participants
CREATE TABLE IF NOT EXISTS participants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    profession VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    role_id INT REFERENCES roles(id) ON DELETE SET NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Table des sessions
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    heure_debut TIMESTAMP NOT NULL,
    heure_fin TIMESTAMP NOT NULL,
    conferenciers TEXT NOT NULL,
    salle VARCHAR(100) NOT NULL
);

-- Table des questions
CREATE TABLE IF NOT EXISTS questions (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    status VARCHAR(20) DEFAULT 'non_repondu',
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    participant_id INTEGER REFERENCES participants(id) ON DELETE SET NULL,
    orateur_id INTEGER REFERENCES orateurs(id) ON DELETE SET NULL
);

-- Table d'association many-to-many sessions <-> orateurs
CREATE TABLE IF NOT EXISTS session_orateurs (
    session_id INT NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    orateur_id INT NOT NULL REFERENCES orateurs(id) ON DELETE CASCADE,
    PRIMARY KEY (session_id, orateur_id)
);

-- Contrainte de clé étrangère (SET NULL si on supprime l'orateur)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_name = 'questions_orateur_id_fkey'
          AND table_name = 'questions'
    ) THEN
        ALTER TABLE questions
            ADD CONSTRAINT questions_orateur_id_fkey
            FOREIGN KEY (orateur_id) REFERENCES orateurs(id) ON DELETE SET NULL;
    END IF;
END $$;


CREATE INDEX IF NOT EXISTS idx_questions_session ON questions(session_id);
CREATE INDEX IF NOT EXISTS idx_questions_orateur ON questions(orateur_id);
CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(heure_debut, heure_fin);

-- Insertion des rôles de base
INSERT INTO roles (nom) VALUES ('participant')
    ON CONFLICT (nom) DO NOTHING;
INSERT INTO roles (nom) VALUES ('moderateur')
    ON CONFLICT (nom) DO NOTHING;
INSERT INTO roles (nom) VALUES ('admin')
    ON CONFLICT (nom) DO NOTHING;

INSERT INTO orateurs (nom) VALUES
('Dr Alice Dupont'),
('Pr Bob Martin'),
('Dr Chloé Bernard'),
('Dr Idriss Ben Ali'),
('Pr Fatou Ndiaye'),
('Dr Jean-Pierre Rocard'),
('Dr Maria Sanchez'),
('Pr Ahmed El Amrani'),
('Dr Sophie Nguyen'),
('Pr Luca Rossi');

INSERT INTO sessions (titre, heure_debut, heure_fin, conferenciers, salle)
VALUES
('Session A — IA clinique',
 NOW() - INTERVAL '30 minutes',
 NOW() + INTERVAL '90 minutes',
 'Dr Alice Dupont,Pr Bob Martin',
 'A1');

-- À venir (dans 2h, dure 2h)
INSERT INTO sessions (titre, heure_debut, heure_fin, conferenciers, salle)
VALUES
('Session B — Données & Santé',
 NOW() + INTERVAL '2 hours',
 NOW() + INTERVAL '4 hours',
 'Dr Chloé Bernard',
 'B1');

-- Passée (terminée il y a ~3h)
INSERT INTO sessions (titre, heure_debut, heure_fin, conferenciers, salle)
VALUES
('Session C — Sécurité',
 NOW() - INTERVAL '5 hours',
 NOW() - INTERVAL '3 hours',
 'Dr Idriss Ben Ali',
 'C1');

-- (re)tirage : on efface d'abord les liens existants (facultatif)
TRUNCATE TABLE session_orateurs;

-- Pour chaque session, on choisit 1 à 3 orateurs au hasard
INSERT INTO session_orateurs (session_id, orateur_id)
SELECT s.id, o.id
FROM sessions s
CROSS JOIN LATERAL (
  SELECT id
  FROM orateurs
  ORDER BY random()
  LIMIT 2
) o
ON CONFLICT DO NOTHING;