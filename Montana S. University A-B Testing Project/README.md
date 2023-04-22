## A/B Testing - Montana State University | Python

### Project Objectives & Overview
#### 1. Overview
The Library of Montana State University has a website that students use to find books and articles.

<img width="1221" alt="Screen Shot 2023-04-22 at 6 42 57 PM" src="https://user-images.githubusercontent.com/90986708/233796469-6bb38ade-83e8-4915-ae69-92efefd4a713.png">

Below the library picture, there is a search bar and three big items: “Find”, “Request” and “Interact”. All three of them contain access to important information and services about the library. However, the Website Analytics show that the “Interact” button has, ironically, almost no interactions.

<img width="1221" alt="Screen Shot 2023-04-22 at 6 42 26 PM" src="https://user-images.githubusercontent.com/90986708/233796479-21af44a2-006b-4d46-ae74-f4aee4186a04.png">


The way to measure how each one of the three categories performs is by click-through rate (CTR), a common term in Online Marketing which typically describes the number of clicks an ad receives divided by the number of times the ad is shown.

#### 2. Purpose of the Project

The main purpose of this project is to create an A/B test to compare the performance of two or more versions of the website.


After the interviews with the users and some brainstorming, the website team settled on 4 different new versions to test against the original “Interact” button:


After discussions with users and some brainstorming, the website team decided on 4 different new versions to test against the "Interaction" button:

- Connect
- Learn
- Help
- Services

The metrics to track were following:

- **Click-through rate (CTR) for the homepage:** Amount of clicks on the button divided by the total visits to the page. Selected as a measure of the initial ability of the category title to attract users.

- **Drop-off rate for the category pages:** Percentage of visitors who leave the site from a given page, selected as a measure of the ability of the category page to meet user expectations.

- **Homepage-return rate for the category pages:** Percentage of users who navigated from the library homepage to the category page, then returned back to the homepage. Homepage-return rate was therefore selected as a measure of the ability of the category page to meet user expectations.


#### 3. Technical Skills

- Python (Pandas)

#### 4. Conclusions

- "SERVICES" shows the best CTR of all options (although when compared to "CONNECT" not statistically significant) and has a ZERO PERCENT drop-off/homepage-return-rate.

- Students likes Services version more, rather than Connect.

- Homepage-return rate: The Services version is better at giving information to users they want.

- Therefore it's strongly advised to change the library's homepage and roll out the design with the "SERVICES"-button.
