CREATE TABLE IF NOT EXISTS product (
    item_sk INT PRIMARY KEY,
    item_id INT UNIQUE,
    item_name VARCHAR(255),
    item_category VARCHAR(100),
    item_price DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS customer (
    customer_sk INT PRIMARY KEY,
    customer_id INT UNIQUE,
    customer_name VARCHAR(255),
    customer_address VARCHAR(255),
    customer_city VARCHAR(100),
    customer_state VARCHAR(100),
    customer_zip VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS store_sales (
    ss_ticket_number INT PRIMARY KEY,
    ss_sold_date_sk INT,
    ss_sold_time_sk INT,
    ss_item_sk INT,
    ss_customer_sk INT,
    ss_cdemo_sk INT,
    ss_hdemo_sk INT,
    ss_addr_sk INT,
    ss_store_sk INT,
    ss_promo_sk INT,
    ss_quantity INT,
    ss_wholesale_cost DECIMAL(10,2),
    ss_list_price DECIMAL(10,2),
    ss_sales_price DECIMAL(10,2),
    ss_ext_discount_amt DECIMAL(10,2),
    ss_ext_sales_price DECIMAL(10,2),
    ss_ext_wholesale_cost DECIMAL(10,2),
    ss_ext_list_price DECIMAL(10,2),
    ss_ext_tax DECIMAL(10,2),
    ss_coupon_amt DECIMAL(10,2),
    ss_net_paid DECIMAL(10,2),
    ss_net_paid_inc_tax DECIMAL(10,2),
    ss_net_profit DECIMAL(10,2)
);

INSERT INTO customer (customer_sk, customer_id, customer_name, customer_address, customer_city, customer_state, customer_zip) VALUES
(5001, 1001, 'Alice Smith', '123 Maple Street', 'Springfield', 'IL', '62704'),
(5002, 1002, 'Bob Johnson', '456 Oak Avenue', 'Lincoln', 'NE', '68508'),
(5003, 1003, 'Carol Williams', '789 Pine Road', 'Madison', 'WI', '53703');

INSERT INTO product (item_sk, item_id, item_name, item_category, item_price) VALUES
(1001, 2001, 'Laptop', 'Electronics', 999.99),
(1002, 2002, 'Smartphone', 'Electronics', 599.99),
(1003, 2003, 'Headphones', 'Accessories', 199.99);

INSERT INTO store_sales (
    ss_ticket_number,
    ss_sold_date_sk,
    ss_sold_time_sk,
    ss_item_sk,
    ss_customer_sk,
    ss_cdemo_sk,
    ss_hdemo_sk,
    ss_addr_sk,
    ss_store_sk,
    ss_promo_sk,
    ss_quantity,
    ss_wholesale_cost,
    ss_list_price,
    ss_sales_price,
    ss_ext_discount_amt,
    ss_ext_sales_price,
    ss_ext_wholesale_cost,
    ss_ext_list_price,
    ss_ext_tax,
    ss_coupon_amt,
    ss_net_paid,
    ss_net_paid_inc_tax,
    ss_net_profit
) VALUES
(8001, 2450815, 1345, 1001, 5001, 3001, 4001, 2001, 6001, 7001, 2, 150.00, 200.00, 180.00, 20.00, 160.00, 300.00, 400.00, 15.00, 10.00, 170.00, 185.00, 30.00),
(8002, 2450816, 1015, 1002, 5002, 3002, 4002, 2002, 6002, 7002, 1, 75.50, 120.00, 110.00, 10.00, 100.00, 150.00, 200.00, 8.00, 5.00, 105.00, 113.00, 20.00),
(8003, 2450817, 1230, 1003, 5003, 3003, 4003, 2003, 6003, 7003, 5, 300.00, 450.00, 400.00, 50.00, 350.00, 750.00, 900.00, 25.00, 15.00, 365.00, 390.00, 100.00),
(8004, 2450818, 0945, 1004, 5004, 3004, 4004, 2004, 6004, 7004, 3, 200.00, 320.00, 300.00, 30.00, 270.00, 600.00, 960.00, 20.00, 10.00, 280.00, 300.00, 80.00),
(8005, 2450819, 1600, 1005, 5005, 3005, 4005, 2005, 6005, 7005, 4, 180.00, 250.00, 220.00, 25.00, 195.00, 720.00, 1000.00, 18.00, 12.00, 207.00, 225.00, 90.00),
(8006, 2450820, 1130, 1006, 5006, 3006, 4006, 2006, 6006, 7006, 2, 160.00, 210.00, 190.00, 20.00, 170.00, 480.00, 840.00, 16.00, 8.00, 178.00, 194.00, 70.00),
(8007, 2450821, 1400, 1007, 5007, 3007, 4007, 2007, 6007, 7007, 6, 350.00, 500.00, 450.00, 60.00, 390.00, 1050.00, 1500.00, 30.00, 20.00, 410.00, 440.00, 160.00),
(8008, 2450822, 0800, 1008, 5008, 3008, 4008, 2008, 6008, 7008, 1, 90.00, 130.00, 120.00, 12.00, 108.00, 270.00, 390.00, 9.00, 6.00, 114.00, 123.00, 30.00),
(8009, 2450823, 1500, 1009, 5009, 3009, 4009, 2009, 6009, 7009, 3, 220.00, 300.00, 250.00, 25.00, 225.00, 660.00, 900.00, 22.00, 13.00, 238.00, 260.00, 85.00),
(8010, 2450824, 1030, 1010, 5010, 3010, 4010, 2010, 6010, 7010, 4, 250.00, 400.00, 350.00, 35.00, 315.00, 1000.00, 1600.00, 28.00, 18.00, 333.00, 361.00, 120.00);
