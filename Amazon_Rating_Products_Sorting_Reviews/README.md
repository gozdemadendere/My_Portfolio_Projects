### AMAZON | Calculating Product Ratings & Sorting Customer Reviews

One of the most significant challenges in e-commerce is accurately calculating post-purchase ratings for products (Rating Products). Solving this problem enhances customer satisfaction, promotes product visibility for sellers, and ensures a seamless shopping experience for buyers.

Another issue is sorting product reviews accurately (Sorting Reviews). Highlighting misleading reviews can directly impact product sales, resulting in both financial loss and customer dissatisfaction.

Addressing these two fundamental problems not only boosts sales for e-commerce platforms and sellers but also ensures customers complete their purchasing journey. 
______________________________


### 1. BUSINESS PROBLEM / PROJECT OBJECTIVE

This dataset contains data for the product with the most reviews in the Amazon Electronics category, including product categories, various metadata, customer ratings, and reviews.

Our objective is to develop a method for calculating product ratings and to sort customer reviews so that the most useful reviews are placed at the top.

______________________________ 

### 2. PROJECT STEPS
 
1. Business Problem
2. Data Understanding
3. Rating Products
4. Sorting Reviews

______________________________

### 3. PROJECT RESULTS

#### 1) Overall Product Rating Average

The overall product rating average is calculated as 4.58.

<img width="593" alt="Screen Shot 2024-02-14 at 3 13 14 PM" src="https://github.com/gozdemadendere/My_Portfolio_Projects_/assets/90986708/b3c06274-ed88-43bf-98c8-9c28f8be8df6">

__________________________________

#### 2) Time-Based Weighted Average Rating for the Product

Our function calculates the product's time-based weighted average rating based on the date each review/rating was made on Amazon.

Recent ratings receive more weight in the average. This allows new, successful, and trending products to stand out.

The time-based weighted average rating for the product is calculated as 4.69.

<img width="593" alt="Screen Shot 2024-02-14 at 3 13 00 PM" src="https://github.com/gozdemadendere/My_Portfolio_Projects_/assets/90986708/f3adbc1b-e37a-4af8-a7e6-8df7e869c906">


__________________________________

#### 3) Sorting Customer Reviews

The most useful customer reviews/evaluations are sorted at the top based on Wilson Lower Bound statistical scores. (These scores increase proportionally with the reliability of the reviewing customers and the number of other customers who liked the review.)

These reviews can guide users in making informed purchasing decisions.

<img width="593" alt="Screen Shot 2024-02-14 at 3 17 48 PM" src="https://github.com/gozdemadendere/My_Portfolio_Projects_/assets/90986708/c0cf480e-1ff1-48d8-9676-18bd532fae5a">


__________________________________
### Conclusion:

Overall, this project underscores the importance of a data-driven approach in overcoming key challenges in e-commerce. It can ultimately lead to increased customer satisfaction, enhanced trust in the relevant e-commerce platform and seller, and improved product and review visibility.


** My Medium article about this project:
[Rating Products & Sorting Reviews on Amazon](https://medium.com/python-in-plain-english/rating-products-sorting-reviews-in-amazon-e7d7b1908d41)

