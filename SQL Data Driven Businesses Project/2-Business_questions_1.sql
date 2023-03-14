
USE magist;

-- 1) How many orders are there in the dataset?

SELECT COUNT(*) AS orders_count
FROM orders;


-- 2) Are orders actually delivered?

SELECT order_status, COUNT(*) AS orders
FROM orders
GROUP BY order_status;


-- 3) Is Magist having user growth?

SELECT
YEAR(order_purchase_timestamp) AS year_,
MONTH(order_purchase_timestamp) AS month_,
COUNT(customer_id)
FROM orders
GROUP BY year_ , month_
ORDER BY year_ , month_;



-- 4) How many products are there in the products table?

SELECT COUNT(DISTINCT product_id) AS products_count
FROM products;


-- 5) Which are the categories with most products?

SELECT product_category_name_translation.product_category_name_english ,COUNT(products.product_id), (COUNT(product_id) / (SELECT COUNT(*)  FROM products)*100) AS Percentage
FROM products
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY COUNT(products.product_id) DESC;


-- 6) How many of those products were present in actual transactions?

SELECT COUNT(DISTINCT product_id) AS n_products
FROM order_items;


-- 7)  What’s the price for the most expensive and cheapest products?

SELECT MIN(price) AS cheapest, MAX(price) AS most_expensive
FROM order_items;

SELECT product_category_name_english AS Category, MIN(price) AS cheapest, MAX(price) AS most_expensive
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_english;


-- 8)  What are the highest and lowest payment values?

SELECT MAX(payment_value) as highest, MIN(payment_value) as lowest
FROM order_payments;



