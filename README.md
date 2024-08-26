# COLLEGE FOOTBALL DATA PIPELINE
This is a dynamic data pipeline for accessing all sorts of data from CollegeFootballData.com's API. API keys can be acquired for FREE from the CollegeFootballData.com website.  

Version: v.1.0.10

Author: [Tyler Shepherd](https://github.com/TylerShep)   

Technologies:  
Python
PostgreSQL



## Project Overview:
V.1.0 of this project was aimed to provide an open-source, dynamic solution for getting data from the CFBD REST API to a postgre SQL database.
The project utilizes retriever and pusher serrvices that can be linked to basic endpoint request services, all of which are managed by a requests manger. The mangager runs and updates on a cron schedule.



## Installation & Setup:



## Helpful Resources:
CollegeFootballData.com provides a lot of helpful documention about their API usage, endpoint schema, and data applications:  

CFBD's Github repo: [HERE](https://github.com/CFBD/cfbd-python?tab=readme-ov-file)  

For help with API Endpoint schema, paramaters and more: [HERE](https://api.collegefootballdata.com/api/docs/?url=/api-docs.json#/)  

For help on seeing what raw data looks like when exported: [HERE](https://collegefootballdata.com/exporter)  
