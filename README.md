Event Registration Backend

Overview

A REST API built with Python, Flask, and SQLite for managing registrations for the Backend Development Workshop.

Event Details

Event: Backend Development Workshop
Date: 20 October 2026
Maximum Participants: 50

Technologies Used

Python
Flask
SQLite
REST API
PowerShell for API testing

Features

Register participants with name and email
Accept optional college and department details
Automatically record registration date and time
Prevent duplicate email registrations
Enforce the maximum participant capacity
View all registrations
Find a registration by ID or email
Validate required fields and return meaningful error responses

Setup Instructions

Install Python.
Open a terminal in the project folder.
Install Flask:
python -m pip install flask
Start the application:
python app.py
Open http://127.0.0.1:5000/ in a browser.
The SQLite database and registrations table are created automatically when the application starts.
API Endpoints

Method

Endpoint
Purpose
GET
/
Check whether the API is running
POST
/register
Register a participant
GET
/registrations
View all registrations
GET
/registrations/<id>
Find a registration by ID
GET
/registrations?email=student@example.com
Find a registration by email

Registration Request Example

Send a POST request to /register with JSON:
{
  "name": "Student Name",
  "email": "student@example.com",
  "college": "Example College",
  "department": "CSE"
}
The name and email are required. College and department are optional.

Response Codes

201 Created — Registration successful
400 Bad Request — Missing or invalid input
404 Not Found — Registration does not exist
409 Conflict — Duplicate email or registration capacity reached

Database

SQLite stores participant details, including a unique ID, name, email, college, department, and registration timestamp.

Running Locally

Run python app.py and use a browser or an API client to test the endpoints. The application currently uses Flask's development server and is intended for local demonstration.