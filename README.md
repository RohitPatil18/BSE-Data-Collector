# BhavCopy Equity Engine

BSE publishes a "Bhavcopy" (Equity) ZIP every day [here](https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx). This applications runs a task everyday at 18:00 IST, Downloads the zip and stores the data in Redis database. This data is displayed on a dashboard.

Demo link: 

Following functionalities are working on Dashboard

* Listing of Stocks
* Searching for specific stock info by name
* Download the results in .csv format

## This application is build with following framework/libraries

* Django == 3.1.7
* Celery == 4.4.0
* VueJS
* Redis == 6.2

## Installation Guide

1. Install Docker engine (and docker-compose) on your machine. Find guide [here](https://docs.docker.com/engine/install/)
1. Application Configuration
    * Application related configuration should be stored in .env file in bse_data_collector folder.
    * Copy template.env file to bse_data_collector and rename it to .env. Fill in values for environment variables.
1. Running Project
    * To run dockerized application, Run following command:
        > ```docker-compose build && docker-compose up```
    * Your appliacation will be accessible on port 3100. Open http://127.0.0.1:3100 on your local machine.


Thanks for checking out this project. Let me know for any improvements.
