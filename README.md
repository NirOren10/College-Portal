# CollegePortal
## Descriptio

High students apply to many colleges and have to manage and track many applications at once, open them daily, and check for any changes. This website is built to bring all the info that is scattered across many colleges’ application portals into one website. 

## The Architecture
![alt text](https://github.com/NirOren10/College-Portal/blob/master/architecture.png?raw=true)
In this project’s infrastructure there are three main roles:
The student- the customer, who will be using the service
The admin- works behind the scenes to ensure accuracy
The data extractor- the algorithm to extract data from the user’s logins.

When first registering on the website, the student provides their logins for the colleges. At that moment, the data extractor will safely log in to each of the student’s colleges’ portals, and upload a screenshot of each portal to the database. The admins will later look at each screenshot, and from there upload the data into the student’s account. 

After the initial setup, every X amount of time, the data extractor will iterate over the students and log in to every one of their portals, take a screenshot of the portal, and compare it to the previous screenshot that is saved in the database. 
If the screenshot is the same, there has been no change.
If it has changed, the previous one is replaced with the new one on the database, and it is sent to the admins, that will later update the student’s account.

## The DataBase:

The database contains the following tables:
Users - users of the website(email, password…)
Colleges- All colleges in the US and the URLs to their application portals
Logins- the username and password used by a student to log into an application portal
Checklists- All the details in the application portals (SAT received, Essays, FAFSA…) 

## Built With
Python
pandas
pymongo
Flask
Django
DateTime
NumPy
Selenium
MongoDB
