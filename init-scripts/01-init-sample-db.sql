-- Create a sample table
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO customers (name, email) VALUES
    ('John Doe', 'john.doe@example.com'),
    ('Jane Smith', 'jane.smith@example.com'),
    ('Bob Johnson', 'bob.johnson@example.com'),
    ('Alice Brown', 'alice.brown@example.com'),
    ('Charlie Davis', 'charlie.davis@example.com'),
    ('Eva Wilson', 'eva.wilson@example.com'),
    ('Frank Miller', 'frank.miller@example.com'),
    ('Grace Taylor', 'grace.taylor@example.com'),
    ('Henry Clark', 'henry.clark@example.com'),
    ('Ivy Robinson', 'ivy.robinson@example.com');

-- Create a sample orders table with relationship to customers
CREATE TABLE IF NOT EXISTS orders (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(id),
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) NOT NULL
);

-- Insert sample orders
INSERT INTO orders (customer_id, total_amount, status) VALUES
    (1, 99.99, 'completed'),
    (1, 149.99, 'processing'),
    (2, 35.50, 'completed'),
    (3, 249.99, 'shipped'),
    (4, 59.99, 'completed'),
    (5, 129.99, 'processing'),
    (6, 89.99, 'completed'),
    (7, 199.99, 'shipped'),
    (8, 45.50, 'completed'),
    (9, 79.99, 'processing'),
    (10, 159.99, 'completed'),
    (2, 29.99, 'shipped'),
    (3, 69.99, 'completed'),
    (4, 119.99, 'processing'),
    (5, 49.99, 'completed');

-- Create a sample order_items table
CREATE TABLE IF NOT EXISTS order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id),
    product_name VARCHAR(100) NOT NULL,
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

-- Insert sample order items
INSERT INTO order_items (order_id, product_name, quantity, price) VALUES
    (1, 'Laptop', 1, 899.99),
    (1, 'Mouse', 1, 24.99),
    (2, 'Smartphone', 1, 699.99),
    (2, 'Phone Case', 1, 19.99),
    (3, 'Headphones', 1, 149.99),
    (4, 'Tablet', 1, 349.99),
    (5, 'Keyboard', 1, 59.99),
    (6, 'Monitor', 1, 249.99),
    (7, 'Printer', 1, 199.99),
    (8, 'External Hard Drive', 1, 89.99),
    (9, 'Wireless Earbuds', 1, 129.99),
    (10, 'Smart Watch', 1, 199.99),
    (11, 'USB Cable', 2, 9.99),
    (12, 'Power Bank', 1, 49.99),
    (13, 'Webcam', 1, 79.99),
    (14, 'Gaming Mouse', 1, 69.99),
    (15, 'HDMI Cable', 1, 14.99);