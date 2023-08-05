
# BUSINESS QUESTIONS

USE magist;


##### IN RELATION TO THE PRODUCTS

--  1) How is the technology products distribution Magist have?   (Tech categories considered as: 'telephony', 'computers_accessories','electronics','computers', 'audio')

SELECT product_category_name_english, COUNT(product_id) AS product_count, (COUNT(product_id) / (SELECT COUNT(*) FROM products) *100) AS percentage
FROM products
LEFT JOIN product_category_name_translation
USING (product_category_name)
WHERE product_category_name_english IN('telephony', 'computers_accessories','electronics','computers', 'audio')
GROUP BY product_category_name_english
ORDER BY product_count DESC;


-- 2) How many products of these tech categories have been sold? What percentage does that represent from the overall number of products sold?

SELECT product_category_name_translation.product_category_name_english, COUNT(order_id) AS Order_quantity , ROUND((COUNT(order_id) / (SELECT COUNT(*)  FROM order_items)*100),2) AS Percentage
FROM products
RIGHT JOIN order_items
ON products.product_id = order_items.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY Order_quantity DESC;


--  3) What’s the average price of the products being sold on category-bases?

SELECT product_category_name_english, ROUND( AVG(price), 0) AS average_price
FROM order_items
JOIN products
USING (product_id)
JOIN product_category_name_translation
USING (product_category_name)
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_english
ORDER BY average_price DESC;


--  4) Are expensive tech products popular?

SELECT product_category_name_translation.product_category_name_english, ROUND(AVG(price),0) AS Average_Price, COUNT(order_id) AS Order_quantity,
CASE
WHEN COUNT(order_id) > 3000 THEN "Very Popular"
WHEN COUNT(order_id) < 500 THEN "Less Popular"
ELSE "Popular"
END Popularity
FROM products
RIGHT JOIN order_items
ON products.product_id = order_items.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY Average_Price DESC;


--  5) Which are the top 5 categories with most products? (show category names in English)

SELECT product_category_name_english, COUNT(DISTINCT product_id) AS product_count, ROUND( (COUNT(DISTINCT product_id)/ (SELECT COUNT(*) FROM products)*100) , 2 ) AS percentage
FROM products
LEFT JOIN product_category_name_translation
USING (product_category_name)
GROUP BY product_category_name_english
ORDER BY product_count DESC
LIMIT 5;


--  6) What’s the price for the most expensive and cheapest products?

SELECT MIN(price) AS cheapest , MAX(price) AS most_expensive
FROM order_items;

## Category based
SELECT product_category_name_english AS Category, MIN(price) AS cheapest, MAX(price) AS most_expensive
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_english;


-- 7) How many months of data are included in the magist database?

SELECT timestampdiff(MONTH, (MIN(order_purchase_timestamp)) , MAX(order_purchase_timestamp))
FROM orders;








##### IN RELATION TO THE ORDERS

-- 1) Does Magist have user growth?

# Year based
SELECT YEAR(DATE(order_approved_at)) AS year, COUNT(customer_id) AS number_of_customer
FROM orders
GROUP BY year
ORDER BY year;
## It looks like Magist has user growth. 2016: 322 customers | 2017: 44972 customers | 2018: 53987 customers

# Year & Month based
SELECT YEAR(DATE(order_approved_at)) AS year, MONTH(DATE(order_approved_at)) AS month, COUNT(customer_id) AS number_of_customer
FROM orders
GROUP BY year, month
WITH ROLLUP;








##### IN RELATION TO THE SELLERS

--  1) How many sellers are there? How many Tech sellers are there? What percentage of overall sellers are Tech sellers?

SELECT  tech_sellers_count, all_sellers_count , ( tech_sellers_count / all_sellers_count ) * 100 AS percentage 
FROM 
	(SELECT COUNT( DISTINCT sellers.seller_id) AS  tech_sellers_count,
		(SELECT COUNT(DISTINCT seller_id)
		FROM sellers) AS all_sellers_count 
	FROM sellers
	JOIN order_items
    ON sellers.seller_id = order_items.seller_id
	JOIN products
    ON order_items.product_id = products.product_id
	JOIN product_category_name_translation
    ON products.product_category_name = product_category_name_translation.product_category_name
	WHERE product_category_name_english IN ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')) AS SUB_TABLE;


-- 2) What is the total amount earned by all sellers? What is the total amount earned by all Tech sellers?

SELECT ROUND(sum(price)) as Revenue
FROM order_items;

SELECT product_category_name_english as Category, ROUND(sum(price)) as Revenue
FROM order_items
JOIN products
ON order_items.product_id = products.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english IN ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_english;


--  3) Can you work out the average monthly income of all sellers? Can you work out the average monthly income of Tech sellers?

SELECT ROUND((SELECT SUM(payment_value)
FROM order_payments) / (SELECT (TIMESTAMPDIFF(MONTH, MIN(order_purchase_timestamp), MAX(order_purchase_timestamp)))
FROM orders)) AS avg_monthly_income_all_seller, ROUND(SUM(order_payments.payment_value) / (SELECT (TIMESTAMPDIFF(MONTH,  MIN(order_purchase_timestamp), MAX(order_purchase_timestamp)))
FROM orders)) AS avg_monthly_income_tech_seller
FROM sellers
JOIN order_items
ON sellers.seller_id = order_items.seller_id
JOIN products
ON order_items.product_id = products.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
JOIN order_payments
ON order_items.order_id = order_payments.order_id
WHERE product_category_name_english IN ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio');









#####  IN RELATION TO THE DELIVERY TIME

-- 1) What’s the average time between the order being placed and the product being delivered?

SELECT ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)), 0) AS Average_time_in_days
FROM orders;


-- 2) How many orders are delivered on time vs orders delivered with a delay?

SELECT delivery_status, COUNT(*)
FROM 
(SELECT TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date),
CASE 
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > 0 THEN "delivered with a delay"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) < 0 THEN "delivered earlier"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) = 0 THEN "delivered on time"
ELSE "there are null -order delivered customer date- values"
END delivery_status
FROM orders) AS delivery_table
GROUP BY delivery_status;

    
-- 3) Is there any pattern for delayed orders, e.g. big products being delayed more often?

SELECT count(o.order_id) AS number_of_orders,
CASE
   WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > 0 THEN "delivered with a delay"
   WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) = 0 THEN "delivered on time"
   WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) < 0 THEN "delivered earlier"
   END AS delivery_date_check,
CASE
    WHEN product_weight_g > 19999 THEN 'VERY HEAVY 20kg+'
    WHEN product_weight_g BETWEEN 10000 AND 19999 THEN 'HEAVY 10kg+'
    WHEN product_weight_g BETWEEN 5000 AND 9999 THEN 'MEDIUM 5kg+'
    ELSE 'LIGHT <5kg'
    END AS weight_categories
FROM orders o
RIGHT JOIN order_items oi
ON o.order_id=oi.order_id
RIGHT JOIN products p
ON oi.product_id=p.product_id
GROUP BY delivery_date_check, weight_categories
ORDER BY weight_categories DESC;





##### ADVANCED SQL FUNCTIONS


-- Let’s rank top 10 sellers based on their sales in descending order.

SELECT seller_id, COUNT(order_id) AS total_sales, ROW_NUMBER() OVER(ORDER BY COUNT(order_id) DESC) AS seller_rank
FROM order_items
GROUP BY seller_id
ORDER BY total_sales DESC
LIMIT 10;


-- Find the average price of products for each tech category. (Tech categories considered as: 'telephony', 'computers_accessories','electronics','computers', 'audio')

SELECT product_id, product_category_name_english, AVG(PRICE) OVER(PARTITION BY product_category_name_english) AS category_avg_price
FROM order_items
LEFT JOIN products
USING(product_id)
LEFT JOIN product_category_name_translation
USING(product_category_name)
WHERE product_category_name_english IN ('telephony', 'computers_accessories','electronics','computers', 'audio');


-- Retrieve orders with the highest price.

SELECT order_id, price
FROM order_items
WHERE price = (SELECT MAX(price) FROM order_items);


-- Retrieve orders with the second highest price.

SELECT order_id, price
FROM order_items
WHERE price < (SELECT MAX(price) FROM order_items)
ORDER BY price DESC
LIMIT 1;


-- Calculate the total order for each customer, considering only orders in the year 2017.

CREATE TEMPORARY TABLE table_order_qty
SELECT customer_id, order_delivered_customer_date, COUNT(order_id) OVER (PARTITION BY customer_id) AS order_count
FROM orders;

SELECT customer_id, SUM(CASE WHEN YEAR(order_delivered_customer_date)=2017 THEN order_count ELSE 0 END) AS 2017_order_qty
FROM table_order_qty
GROUP BY customer_id;


-- Find the orders that have not been delivered in the last six months.
SELECT order_id, DATE(order_delivered_customer_date) 
FROM orders
WHERE DATE(order_delivered_customer_date) < (DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH));