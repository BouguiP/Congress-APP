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

INSERT INTO sessions (titre, heure_debut, heure_fin, salle)
VALUES
('Session A ',
  timezone('Europe/Paris', now()) - interval '30 minutes',
  timezone('Europe/Paris', now()) + interval '90 minutes',
  'Salle A1');

INSERT INTO sessions (titre, heure_debut, heure_fin, salle)
VALUES
('Session B ',
  timezone('Europe/Paris', now()) + interval '2 hours',
  timezone('Europe/Paris', now()) + interval '5 hours',
  'Salle B1');

INSERT INTO sessions (titre, heure_debut, heure_fin, salle)
VALUES
('Session C ',
  timezone('Europe/Paris', now()) - interval '5 hours',
  timezone('Europe/Paris', now()) - interval '3 hours',
  'Salle C1');


-- (re)tirage : on efface d'abord les liens existants (facultatif)
TRUNCATE TABLE session_orateurs;

-- Pour chaque session, on choisit 1 à 3 orateurs au hasard
INSERT INTO session_orateurs (session_id, orateur_id)
SELECT s.id, o.id
FROM sessions s
CROSS JOIN LATERAL (
  SELECT id
  FROM orateurs
  WHERE s.id IS NOT NULL
  ORDER BY random()
  LIMIT 2
) o
ON CONFLICT DO NOTHING;

INSERT INTO participants (nom, prenom, email, profession, role_id, password)
VALUES (
    'Modo',
    'Modo',
    'modo@example.com',
    'Moderateur',
    2,
    '123'
);