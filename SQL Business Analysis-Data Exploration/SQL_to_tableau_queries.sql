USE magist;


-- How was the distribution of tech products and non-tech products?

-- Product Quantity Distibution 
WITH cte AS(
SELECT product_id, product_category_name_english,
CASE
	WHEN (product_category_name_english = 'telephony') THEN 'telephony'
	WHEN (product_category_name_english = 'computers_accessories') THEN 'computers_accessories'
	WHEN (product_category_name_english = 'electronics') THEN 'electronics'
	WHEN (product_category_name_english = 'computers') THEN 'computers'
	WHEN (product_category_name_english = 'audio') THEN 'audio'
ELSE 'non-tech products'
END AS 'updated_category'
FROM products
JOIN product_category_name_translation
ON product_category_name_translation.product_category_name=products.product_category_name)

SELECT updated_category, COUNT(product_id) AS product_quantity, ROUND(COUNT(product_id) / (SELECT COUNT(product_id) FROM cte), 2) AS product_quantity_percentage
FROM cte
GROUP BY updated_category
ORDER BY product_quantity DESC;





-- What’s the average price of the products being sold?

-- Average Prices Distibution
WITH cte AS(
SELECT product_category_name_english, price,
CASE
	WHEN (product_category_name_english = 'telephony') THEN 'telephony'
	WHEN (product_category_name_english = 'computers_accessories') THEN 'computers_accessories'
	WHEN (product_category_name_english = 'electronics') THEN 'electronics'
	WHEN (product_category_name_english = 'computers') THEN 'computers'
	WHEN (product_category_name_english = 'audio') THEN 'audio'
ELSE 'non-tech products'
END AS 'updated_category'
FROM products
RIGHT JOIN order_items
USING (product_id)
JOIN product_category_name_translation
USING (product_category_name))

SELECT updated_category, ROUND(AVG(price), 0) AS average_price
FROM cte 
GROUP BY updated_category
ORDER BY average_price DESC;






-- How was the revenue distribution of tech products and non-tech products?

-- Total Revenue Distibution
WITH cte AS(
SELECT product_category_name_english, price,
CASE
	WHEN (product_category_name_english = 'telephony') THEN 'telephony'
	WHEN (product_category_name_english = 'computers_accessories') THEN 'computers_accessories'
	WHEN (product_category_name_english = 'electronics') THEN 'electronics'
	WHEN (product_category_name_english = 'computers') THEN 'computers'
	WHEN (product_category_name_english = 'audio') THEN 'audio'
ELSE 'non-tech products'
END AS 'updated_category'
FROM order_items
JOIN products
USING(product_id)
JOIN product_category_name_translation
USING (product_category_name))

SELECT updated_category, ROUND(SUM(price), 0) AS revenue, ROUND(SUM(price) / (SELECT SUM(price) FROM cte), 2) AS revenue_percentage
FROM cte
GROUP BY updated_category
ORDER BY revenue DESC;





-- Are expensive tech products popular? (Eniac's Avg. Product Price:540 €)
WITH cte AS(
SELECT product_category_name_english, price, order_id,
CASE
	WHEN (product_category_name_english = 'telephony') THEN 'telephony'
	WHEN (product_category_name_english = 'computers_accessories') THEN 'computers_accessories'
	WHEN (product_category_name_english = 'electronics') THEN 'electronics'
	WHEN (product_category_name_english = 'computers') THEN 'computers'
	WHEN (product_category_name_english = 'audio') THEN 'audio'
ELSE 'non-tech products'
END AS 'updated_category'
FROM products
RIGHT JOIN order_items
USING(product_id)
JOIN product_category_name_translation
USING(product_category_name))
SELECT updated_category, ROUND(AVG(price)) AS average_price, COUNT(order_id) AS order_quantity, ROUND(COUNT(order_id) / (SELECT COUNT(order_id) FROM cte), 4) AS percentage
FROM cte
GROUP BY updated_category
ORDER BY average_price DESC;

