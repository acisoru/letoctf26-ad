SELECT pg_advisory_xact_lock(1936748391);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    personal_data TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL,
    name TEXT NOT NULL UNIQUE,
    field TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL,
    user_id INTEGER,
    doctor_name TEXT,
    fio TEXT NOT NULL,
    insurance_num TEXT NOT NULL,
    time TEXT NOT NULL
);

-- Do no change!
INSERT INTO doctors (name, field) VALUES
    ('Ryan Gosling', 'Drive'),
    ('Timothy T. Fox', 'Urology'),
    ('Jennifer H. Plante', 'Cardiology'),
    ('Patricia P. Daniels', 'Dermatology'),
    ('Theresa J. Pesina', 'Pediatrics'),
    ('Betty W. Flemings', 'Psychiatry')
ON CONFLICT (name) DO NOTHING;
