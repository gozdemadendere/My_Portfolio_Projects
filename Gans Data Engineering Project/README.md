## GANS Data Engineering Pipeline with API's | Python

📌 My Medium article about this project: [Data Engineering Pipeline with Python](https://medium.com/@gozdebarin/data-engineering-pipeline-with-python-fb4a23e79af)

### Project Objectives & Overview
#### 1. Business Problem
Gans is a startup developing an e-scooter-sharing system.

It aims to operate in the most populated cities all around the world. In each city, it will have hundreds of e-scooters parked on the streets and allow users to rent them by the minute.

#### 2. Purpose of the Project

The aim of this project is to collect data from external sources that can potentially help Gans to predict e-scooter movement.

#### 3. Steps of the Project

- Data Collection: collect data via web scraping or API (Application Programming Interfaces)
- Data Storage: create a Database on a local MySQL instance and store the collected data there
- Pipeline to the Cloud: use Amazon Web Services (AWS) to move the pipeline to the cloud
- Pipeline Automation: automate the whole data collection and storage process


#### 4. Data Collection

The data is collected from:

- Cities Data -> Wikipedia
- Weather Data -> OpenWeatherMap
- Airports Data -> Rapid API (AeroBox)
- Flights Data -> Rapid API (AeroBox)

#### 5. Technical Skills

- Python (BeautifulSoup, Pandas, Seaborn, Matplotlib)
- Requests (API) & Web Scraping
- Amazon Web Services (AWS)
- SQL, SQLAlchemy (Connect Python with MySQL)

#### 6. Project Summary

The automated data pipeline in the cloud was implemented in the following steps:

- Web scraping on a website (Wikipedia) to collect demographic data
- Using APIs to collect weather, airport, and flight data (OpenWeatherMap & AeroDataBox APIs)
- Creating a database on a local MySQL instance to store data from various data sources
- Moving the script and data to the cloud using Amazon Web Services (AWS) and automating the data development pipeline

