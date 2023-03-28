-- In relation to the products:

 -- 1) What categories of tech products does Magist have?

SELECT product_category_name_english, COUNT(product_id) AS Product_quantity, ROUND((COUNT(product_id) / (SELECT COUNT(*)  FROM products)*100),1) AS Percentage
FROM products
JOIN product_category_name_translation
ON product_category_name_translation.product_category_name=products.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories','electronics','computers', 'audio')
GROUP BY product_category_name_english
ORDER BY COUNT(product_id) DESC;


-- 2) How many products of these tech categories have been sold (within the time window of the database snapshot)? What percentage does that represent from the overall number of products sold?

SELECT product_category_name_translation.product_category_name_english, COUNT(order_id) AS Order_quantity , ROUND((COUNT(order_id) / (SELECT COUNT(*)  FROM order_items)*100),2) AS Percentage
FROM products
RIGHT JOIN order_items
ON products.product_id = order_items.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY COUNT(order_id) DESC;


-- 3) What’s the average price of the products being sold?

SELECT product_category_name_translation.product_category_name_english, ROUND(AVG(price),0) AS Average_Price
FROM products
RIGHT JOIN order_items
ON products.product_id = order_items.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY Average_Price DESC;


-- OK  4) Are expensive tech products popular? *

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


-- In relation to the sellers:

-- 1) How many months of data are included in the magist database?

SELECT TIMESTAMPDIFF(MONTH, min, max) 
FROM
(SELECT MIN(order_purchase_timestamp) min, MAX(order_purchase_timestamp) max
			FROM orders) sub_table;


SELECT TIMESTAMPDIFF(DAY,'2016-09-04' , '2018-10-17');


-- 2) How many sellers are there? How many Tech sellers are there? What percentage of overall sellers are Tech sellers?

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


-- 3) What is the total amount earned by all sellers? What is the total amount earned by all Tech sellers?

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


-- 4) Can you work out the average monthly income of all sellers? Can you work out the average monthly income of Tech sellers?

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



-- In relation to the delivery time:

-- 1) What’s the average time between the order being placed and the product being delivered?

SELECT ROUND(AVG(TIMESTAMPDIFF(DAY, order_purchase_timestamp, order_delivered_customer_date)),2) AS Average_time_in_days
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



SELECT COUNT(DISTINCT o.order_id) AS Order_Quantity, product_category_name_english AS Category,
CASE 
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > 3 THEN "delivered with extreme delay"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > 2 THEN "delivered with 3 day delay"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > 1 THEN "delivered with 2 day delay"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > 0 THEN "delivered with 1 day delay"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) = 0 THEN "delivered on time"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) < 0 THEN "delivered 1 day early"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) < -1 THEN "delivered 2 days early"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > -2 THEN "delivered 3 days early"
WHEN (TIMESTAMPDIFF (DAY, order_estimated_delivery_date,order_delivered_customer_date)) > -3 THEN "delivered 4 days early"
ELSE "delivered extremely early"
END AS delivery_status
FROM orders o
RIGHT JOIN
    order_items oi
ON
    o.order_id=oi.order_id
RIGHT JOIN
    products p
ON
    oi.product_id=p.product_id
INNER JOIN
    product_category_name_translation trans
ON
    trans.product_category_name=p.product_category_name
GROUP BY
    product_category_name_english, delivery_status WITH ROLLUP
HAVING
    product_category_name_english in ("computers_accessories", "telephony", "electronics", "audio", "computers", "pc gamer");
    
    
    

-- OK  3) Is there any pattern for delayed orders, e.g. big products being delayed more often?

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


