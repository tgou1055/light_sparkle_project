CREATE SCHEMA IF NOT EXISTS instacart;

SET search_path TO instacart;

-- Create asiles table and insert data
CREATE TABLE aisles (
    aisle_id INT PRIMARY KEY,
    aisle VARCHAR(70) NOT NULL
);

COPY instacart.aisles(aisle_id, aisle) 
FROM '/simulation_data/aisles/aisles.csv' DELIMITER ','  CSV HEADER;

-- Create departments table and insert data
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department VARCHAR(70) NOT NULL
);

COPY instacart.departments(department_id, department) 
FROM '/simulation_data/departments/departments.csv' DELIMITER ','  CSV HEADER;

-- Create products table and insert data
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(200) NOT NULL,
    aisle_id INT REFERENCES aisles(aisle_id) ON DELETE CASCADE,
    department_id INT REFERENCES departments(department_id) ON DELETE CASCADE  
);

COPY instacart.products(product_id, product_name, aisle_id, department_id) 
FROM '/simulation_data/products/products.csv' DELIMITER ','  CSV HEADER;

-- Create orders table and insert data
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    eval_set VARCHAR(10) NOT NULL,
    order_number SMALLINT NOT NULL,
    order_dow SMALLINT NOT NULL,
    order_hour_of_day SMALLINT NOT NULL,
    days_since_prior_order FLOAT
);

COPY instacart.orders(order_id, 
                      user_id, 
                      eval_set, 
                      order_number,
                      order_dow,
                      order_hour_of_day,
                      days_since_prior_order
                      ) 
FROM '/simulation_data/orders/orders.csv' DELIMITER ','  CSV HEADER;
