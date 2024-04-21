## Customer Segmentation with RFM Analysis

RFM analysis is a technique used for customer segmentation, utilizing Recency, Frequency, and Monetary metrics.

It allows for segmenting customers based on their purchasing habits and enables the development of strategies tailored to these segments.

- Recency = Analysis date - Customer's last purchase date
- Frequency = Total number of purchases by the customer (total transactions or invoice count)
- Monetary = Total amount spent by the customer 

______________________________


### 1. Business Problem / Project Objective

FLO, one of the leading companies in the Turkish shoe market, aims to segment its customers based on their purchasing habits and develop strategies tailored to these segments.

The dataset consists of information derived from the past shopping behaviors of customers who made their last purchases OmniChannel (both online and offline shopping) in the years 2020 - 2021.


______________________________

### 2. Project Stages

1. Data Understanding
2. Data Preparation
3. Calculating RFM Metrics: Recency, Frequency, Monetary columns
4. Calculating RFM Scores
5. Creating & Analyzing RFM Segments

______________________________

### 3. Project Results

#### Question 1:

What are the created Customer Segments & Segment-Based Recency, Frequency, and Monetary Averages?

<img width="650" alt="Screen Shot 2024-02-07 at 11 46 30 AM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/7594c4ab-b765-4d3a-b91a-8dd416f2455c">


<img width="665" alt="Screen Shot 2024-02-27 at 10 45 41 PM" src="https://github.com/gozdemadendere/My_Portfolio_Projects_/assets/90986708/3862ac9b-da8d-4889-8cd2-d7555db20fc2">



Customer Segment Recommendations:
- Champions: Most valuable customers. Their satisfaction can be increased with special incentives and VIP customer programs.
- Loyal Customers: Customers who make regular purchases. Products and services tailored to their existing shopping habits can be recommended to increase sales.
- Potential Loyalists: Customers with the potential to become loyal. They can be encouraged to make more purchases with special offers.
- Promising: Customers with potential value. Their interest can be drawn with new products or campaigns.
- New Customers: Welcome offers can be provided to new customers, and discounts can be offered on their first purchases.
- Need Attention: Dissatisfied or complaining customers. Special attention should be given to resolving their issues, and solutions like refunds or exchanges can be offered.
- Can't Lose: Customers at risk of potential loss. Special offers can be provided to retain them.
- At Risk: Customers at risk of being lost. Efforts can be made to regain them with special discounts or campaigns.
- About to Sleep: Customers who make few purchases. Special offers can be provided to activate them.
- Hibernating: Former customers who are not making purchases. Special offers and reminders can be sent to re-engage them.
__________________________________

#### Question 2:

FLO wants to reach out specifically to customers interested in the promotion and sales of a new women's shoe brand, who are "loyal customers (champions, loyal_customers)" and those who shop in the women's category. Find the IDs of these customers.


<img width="600" alt="Screen Shot 2024-02-07 at 12 10 33 PM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/10ef2888-7a8d-4f5e-96e8-873c1adef770">

__________________________________


#### Question 3:
FLO plans to offer a discount of nearly 40% on men's and children's products.

They want to target "past good customers who haven't shopped for a long time" and "new customers" interested in these categories. Find the IDs of these customers.

<img width="600" alt="Screen Shot 2024-02-07 at 12 09 42 PM" src="https://github.com/gozdemadendere/miuul_data_science_bootcamp/assets/90986708/2e3f94fb-2677-4932-b06e-b0994ca90052">


__________________________________
### Conclusion:
Through RFM analysis in this project, the company can develop marketing strategies and establish stronger relationships with customers for long-term success.

