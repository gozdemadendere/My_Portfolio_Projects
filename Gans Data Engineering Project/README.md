## GANS | Data Pipeline with API's and Amazon AWS
### 1. PROJECT OBJECTIVES & OVERVIEW
#### 1.1. INTRODUCTION
Gans is a startup developing an e-scooter-sharing system. My task was to collect data from external sources that can potentially help Gans to predict e-scooter movement.

The purpose of this project is to learn dealing with API's and JSON files. Data had to be requested, structured, and visualized. First a database is built in mySQL Workbench based on the data. Then the scripts are transferred to the cloud (Amazon Web Services) and scheduled to be executed every 24 hours. Iteratively, an SQL database of weather and flight-information is built in the cloud.

📢📢📢 There is a Medium article about this project at:

#### 1.2. STEPS OF THE PROJECT
The main objective of my project is to learn the data engineering process which contains:

- Collect data: data collection via web scraping or Application Programming Interfaces (APIs)
- Set up a local database on MySQL: a database creation in MySQL for data storage
- Create a Data Pipeline to the Cloud: use Amazon Web Services (AWS) to move the pipeline to the cloud
- Automate the Data Pipeline: automate the whole data collection and storage process

#### 1.3. DATASET
The data gathered is freely available:

Cities Data -> Wikipedia

Weather Data -> OpenWeatherMap

Airports Data -> Rapid API (AeroBox)

Flights Data -> Rapid API (AeroBox)

#### 1.4. METHODS & TECHNOLOGIES
🔹 Methods Used

API-Calls

Data Engineering

Data Visualization

Cloud Computin

Cloud Database

🔹 Technologies

Python

Pandas

BeautifulSoup

Jupyter Notebook

Requests (api)

Matplotlib

Amazon Webservices

SQL

Sqlalchemy
