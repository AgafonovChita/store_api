CREATE TABLE products (
        id SERIAL NOT NULL,
        header TEXT,
        description TEXT,
        price FLOAT,
        PRIMARY KEY (id)
);


CREATE TABLE users (
        id BIGSERIAL NOT NULL,
        login TEXT NOT NULL,
        password BYTEA NOT NULL,
        is_active BOOLEAN,
        is_admin BOOLEAN,
        PRIMARY KEY (id),
        UNIQUE (login)
);

INSERT INTO products (header, description, price) VALUES ('Core i7', 'Proccessor PC', 200.0);
INSERT INTO products (header, description, price) VALUES ('Core i3', 'Proccessor PC', 150.0);
INSERT INTO products (header, description, price) VALUES ('Core i5', 'Proccessor PC', 180.0);
INSERT INTO products (header, description, price) VALUES ('Core Duo', 'Proccessor PC', 100.0);

INSERT INTO users (id, login, password, is_active, is_admin) VALUES (777, 'admin', '$2b$12$/GCIt4Aey/GCt8qbjY5tiegYNVM.B3Gu8UOHY3QZ9bPPHeJ3Uex9S'::bytea, True, True);
INSERT INTO users (id, login, password, is_active, is_admin) VALUES (555, 'agafonov', '$2b$12$/GCIt4Aey/GCt8qbjY5tiegYNVM.B3Gu8UOHY3QZ9bPPHeJ3Uex9S'::bytea, True, False);






