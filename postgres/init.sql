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


CREATE TABLE wallets (
        id BIGSERIAL NOT NULL, 
        balance INTEGER, 
        owner_id BIGINT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(owner_id) REFERENCES users (id)
);

CREATE TABLE refresh_tokens (
        id BIGSERIAL NOT NULL, 
        token TEXT NOT NULL, 
        exp BIGINT NOT NULL, 
        PRIMARY KEY (id)
);




CREATE TABLE transactions (
        id BIGSERIAL NOT NULL, 
        amount FLOAT NOT NULL, 
        wallet_id BIGINT, 
        PRIMARY KEY (id), 
        FOREIGN KEY(wallet_id) REFERENCES wallets (id)
);




INSERT INTO products (header, description, price) VALUES ('Core i7', 'Proccessor PC', 200.0);
INSERT INTO products (header, description, price) VALUES ('Core i3', 'Proccessor PC', 150.0);
INSERT INTO products (header, description, price) VALUES ('Core i5', 'Proccessor PC', 180.0);
INSERT INTO products (header, description, price) VALUES ('Core Duo', 'Proccessor PC', 100.0);

INSERT INTO users (id, login, password, is_active, is_admin) VALUES (777, 'admin', '$2b$12$/GCIt4Aey/GCt8qbjY5tiegYNVM.B3Gu8UOHY3QZ9bPPHeJ3Uex9S'::bytea, True, True);
INSERT INTO users (id, login, password, is_active, is_admin) VALUES (555, 'agafonov', '$2b$12$/GCIt4Aey/GCt8qbjY5tiegYNVM.B3Gu8UOHY3QZ9bPPHeJ3Uex9S'::bytea, True, False);

INSERT INTO wallets(id, balance, owner_id) VALUES (7779, 1000, 777);
INSERT INTO wallets(id, balance, owner_id) VALUES (7770, 20, 777);
INSERT INTO wallets(id, balance, owner_id) VALUES (5559, 100, 555);
INSERT INTO wallets(id, balance, owner_id) VALUES (5551, 999, 555);
INSERT INTO wallets(id, balance, owner_id) VALUES (5552, 1000000, 555);




