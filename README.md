# data_representation_project
Project Repository for DATA REPRESENTATION module

# Overview
Please note that a live version of the API built for this project, the app that consumes it, and the web interface are available at the below address:
http://chogandatarep.pythonanywhere.com/ticketviewer.html

In order to access the live version of the project you will need to first login with the below credentials:
USERNAME: admin
PASSWORD: letmein123

This repository contains the following files:

## ticketviewer.html
*This is the homepage for the web interface that interacts with the API.
*It allows a user to create a "help desk ticket" with the following values.
	1. Company name
	2. Description of the ticket
	3. Priority (High, Medium, Low)
*A ticket "Owner" is automatically assigned from a list of 5 possible help desk operators.
*A list of tickets is displayed in a table where they can be updated or deleted.

## dashboard.html
*This page displays a summary table of the ticket Owners and the count of tickets that have been assigned to them.
*There is also the option to generate a pie chart built using D3.js. This shows a breakdown tickets by Priority. 

## ticketDAO.py
*This file contains the code used to interact with the database hosted on Pythonanywhere
*The credentials to access the database are stored in the linked "appconfig.py" file.
*The ticketDAO is used to perform the following SQL commands:
	1. insert a new ticket into the tickets table and randomly assign an Owner from one of 5 options by adding an ownerid value (create function) 
	2. get all values from the tickets table and get the assigned owners firstname and lastname from the owners table (getAll function) 
	3. get a singles tickets values based on the tickets Id and get assigned owners firstname and lastname. (findByID function)
	4. update an individual ticket (update function)
	5. delete an individual ticket (delete function)
	6. get the count of tickets for each priority (getCount function)
	7. get the counts of tickets assigned to each ticket owner (getCountPerOwner function)
	
## application.py
*This file contains the code for the API
*Each of the SQL commands outlined above has a corresponding route where the information is posted before being displayed on the web interface or applied to the database.

## appconfig.py
*File containing credentials for the Pythonanywhere SQL database and the username and password that must be entered to gain access to the API.

## requirements.txt
*Contains the list of packages that need to be installed in order for the Flask server to work.


