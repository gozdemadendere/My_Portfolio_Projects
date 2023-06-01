
USE magist;

-- 1) How many orders are there in the dataset?

SELECT COUNT(*) AS orders_count
FROM orders;
## 99441



-- 2) Are orders actually delivered?

SELECT order_status, COUNT(order_id) AS count_of_order, (COUNT(order_id) / (SELECT COUNT(*) FROM orders))*100 AS percentage
FROM orders
GROUP BY order_status
ORDER BY count_of_order DESC;
## 97% of orders are delivered 



-- 3) Is Magist having user growth?

-- Year & Month based
SELECT YEAR(DATE(order_approved_at)) AS year, MONTH(DATE(order_approved_at)) AS month, COUNT(customer_id) AS number_of_customer
FROM orders
GROUP BY year, month
WITH ROLLUP;
## It looks like Magist has user growth. 2016: 322 customers | 2017: 44972 customers | 2018: 53987 customers


-- Year based
SELECT YEAR(DATE(order_approved_at)) AS year, COUNT(customer_id) AS number_of_customer
FROM orders
GROUP BY year;



-- 4) How many products are there in the products table?

SELECT COUNT(DISTINCT product_id) AS products_count
FROM products;
## There are 32951 products


-- 5) Which are the categories with most products?

SELECT product_category_name_translation.product_category_name_english, COUNT(DISTINCT products.product_id) AS product_count, (COUNT(DISTINCT products.product_id)/ (SELECT COUNT(*) FROM products)*100) AS percentage
FROM products
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
GROUP BY product_category_name_english
ORDER BY percentage DESC;
## bed_bath_table, sports_leisure, furniture_decor



-- 6)  What’s the price for the most expensive and cheapest products?

SELECT MIN(price) AS cheapest, MAX(price) AS most_expensive
FROM order_items;
## Cheapest: 0.85
## Most expensive: 6735

-- Category based
SELECT product_category_name_english AS Category, MIN(price) AS cheapest, MAX(price) AS most_expensive
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_english;



