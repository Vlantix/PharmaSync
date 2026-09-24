CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'manager', 'pharmacist')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drugs(
    id SERIAL PRIMARY KEY,
    generic_name VARCHAR(200) NOT NULL,
    brand_name VARCHAR(200),
    category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    description TEXT,
    unit VARCHAR(20) NOT NULL,
    price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE drugs ADD COLUMN barcode VARCHAR(100) UNIQUE;

CREATE TABLE inventory(
    id SERIAL PRIMARY KEY,
    drug_id INTEGER NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL DEFAULT 0,
    batch_number VARCHAR(100),
    expiry_date DATE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(drug_id, batch_number)
);

CREATE TABLE stock_thresholds (
    id SERIAL PRIMARY KEY,
    drug_id INTEGER NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    min_quantity INTEGER NOT NULL DEFAULT 10,
    updated_by INTEGER REFERENCES users(id),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(drug_id)
);

CREATE TABLE inventory_transactions(
    id SERIAL PRIMARY KEY,
    drug_id INTEGER NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    performed_by INTEGER NOT NULL REFERENCES users(id),
    transaction_type  VARCHAR(20) NOT NULL CHECK (transaction_type IN ('stock_in', 'stock_out', 'dispense', 'adjustment')),
    quantity INTEGER NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE alerts(
    id SERIAL PRIMARY KEY,
    drug_id INTEGER NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    alert_type VARCHAR(20) NOT NULL CHECK (alert_type IN ('low_stock', 'expiry')),
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP
);

CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    performed_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    target_table VARCHAR(50) NOT NULL,
    target_id INTEGER,
    old_data JSONB,
    new_data JSONB,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);