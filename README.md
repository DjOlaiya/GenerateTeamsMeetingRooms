# GenerateTeamsMeetingRooms 


We will be using MS Graph API.

## Work Flow (diagram to come)

Web Client needs to create a meeting room -> Client calls our App -> We call MS Graph Create Events API -> pass Meeting details to client at API endpoint.

## USE CASE
For scenarios where calling MS Graphs API directly is not feasible within a large organization where security makes it difficult to gain the necessary permissions, or for any scenarios where multiple clients want to generate meeting rooms. Eliminates the need to register multiple apps.

## Setup

Install Requirements
 ~~~~
$ pip install -r requirements.txt 
 ~~~~
## Run the Application

In the project directory:
 ~~~~
$ flask run
 ~~~~
Open [http://localhost:5000](http://localhost:5000)


This launches a very simple builtin server, which is good enough for testing but probably not what you want to use in production. For deployment options see [Deployment Options](https://flask.palletsprojects.com/en/1.1.x/deploying/#).

## Learn More

https://flask.palletsprojects.com/en/1.1.x/