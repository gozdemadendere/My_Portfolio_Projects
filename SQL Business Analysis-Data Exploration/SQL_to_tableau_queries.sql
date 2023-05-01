USE magist;


-- Product Quantity Distibution (How was the distribution of tech products and non-tech products?)

SELECT product_category_name_english, COUNT(product_id) AS Product_quantity,
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
ON product_category_name_translation.product_category_name=products.product_category_name
GROUP BY product_category_name_english
ORDER BY COUNT(product_id) DESC;




-- Average Prices Distibution (What’s the average price of the products being sold?)
SELECT product_category_name_translation.product_category_name_english, ROUND(AVG(price),0) AS Average_Price,
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
ON products.product_id = order_items.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY Average_Price DESC;




-- Total Revenue Distibution (How was the revenue distribution of tech products and non-tech products?)

SELECT product_category_name_english as Category, ROUND(sum(price)) as Revenue,
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
ON order_items.product_id = products.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
GROUP BY product_category_name_english;




-- Are expensive tech products popular? (Eniac's Avg. Product Price:540 €)
SELECT product_category_name_translation.product_category_name_english, ROUND(AVG(price),0) AS Average_Price, COUNT(order_id) AS Order_quantity,
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
ON products.product_id = order_items.product_id
JOIN product_category_name_translation
ON products.product_category_name = product_category_name_translation.product_category_name
WHERE product_category_name_english in ('telephony', 'computers_accessories', 'electronics', 'computers', 'audio')
GROUP BY product_category_name_translation.product_category_name_english
ORDER BY Average_Price DESC;

