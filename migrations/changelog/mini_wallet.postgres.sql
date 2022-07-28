--liquibase formatted sql


--changeset robert.julianto:add-table-wallet
CREATE TABLE ${database.defaultSchemaName}.wallet
(
    id VARCHAR NOT NULL
        CONSTRAINT wallet_pk
            PRIMARY KEY,
    owner_id VARCHAR NOT NULL,
    token VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    enabled_at TIMESTAMPTZ,
    disabled_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by VARCHAR DEFAULT USER,
    updated_at TIMESTAMPTZ,
    updated_by VARCHAR,
    CONSTRAINT wallet_unique UNIQUE(owner_id)
);

--changeset robert.julianto:add-table-transaction
CREATE TABLE ${database.defaultSchemaName}.transaction(
    id VARCHAR NOT NULL
        CONSTRAINT transaction_pk
            PRIMARY KEY,
    wallet_id VARCHAR NOT NULL
      CONSTRAINT transaction__wallet_id__fk
        REFERENCES ${database.defaultSchemaName}.wallet,
    type VARCHAR NOT NULL,
    status VARCHAR NOT NULL,
    amount NUMERIC NOT NULL,
    reference_id VARCHAR NOT NULL,
    transaction_time TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_by VARCHAR DEFAULT USER,
    updated_at TIMESTAMPTZ,
    updated_by VARCHAR,
    CONSTRAINT transaction_unique UNIQUE(type, reference_id)
);
