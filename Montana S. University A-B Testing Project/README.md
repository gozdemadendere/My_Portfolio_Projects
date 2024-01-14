## A/B Testing - Montana University Website Homepage | Python
📌 My Medium article: [A/B Testing for Data Scientists](https://medium.com/@gozdebarin/a-b-testing-for-data-scientists-96c50791b0ad)

### Project Objectives & Overview
#### 1. Overview
The Montana State University Library has a website that students use to find books and articles.

Below the library picture, there is a search bar and three big items: “Find”, “Request” and “Interact”. All three of them contain access to important information and services about the library. However, the Website Analytics show that the “Interact” button has, ironically, almost no interactions.

<img width="1221" alt="Screen Shot 2023-04-22 at 6 42 57 PM" src="https://user-images.githubusercontent.com/90986708/233796469-6bb38ade-83e8-4915-ae69-92efefd4a713.png">


The way to measure how each one of the three categories performs is by click-through rate (CTR), a common term in Online Marketing which typically describes the number of clicks an ad receives divided by the number of times the ad is shown.

#### 2. Purpose of the Project 

The main purpose of this project is to perform an A/B Test to check CTR (click-through rate) for different text on a button on the website of Montana S. University.

The website team decided on 4 different new versions to test against the "Interaction" button:

- Connect
- Learn
- Help
- Services

The metrics to track were following:

- **Click-through rate (CTR) for the homepage:** Amount of clicks on the button divided by the total visits to the page. Selected as a measure of the initial ability of the category title to attract users.

- **Drop-off rate for the category pages:** Percentage of visitors who leave the site from a given page, selected as a measure of the ability of the category page to meet user expectations.

- **Homepage-return rate for the category pages:** Percentage of users who navigated from the library homepage to the category page, then returned back to the homepage. Homepage-return rate was therefore selected as a measure of the ability of the category page to meet user expectations.

#### 3. Steps of the Project

- Explore and prepare the data
- Define the hypothesis
- Divide the users into groups
- Collect data from both groups
- Analyze the results
- Test the hypothesis
- Draw conclusions

#### 3. Technical Skills

- Python (Pandas)

#### 4. Conclusions

It is strongly advised to change the library's homepage and roll out the design with the "**Services**" button according to the following reasons:

- **Services** shows the best click-through rate (CTR) of all options.

- **Services** version is better at giving information to users they want as it has a lower Homepage-return Rate.

- Students likes **Services** version more, rather than Connect.


