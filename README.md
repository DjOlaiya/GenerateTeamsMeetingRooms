# GenerateTeamsMeetingRooms 


We will be using MS Graph API.

## Work Flow (diagram to come)

Web Client needs to create a meeting room -> Client calls our App -> We call MS Graph Create Events API -> pass Meeting details to client at API endpoint.

## USE CASE
For scenarios where calling msgraph directly is not feasible within a large organization where security makes it difficult to gain the necessary permissions, or for any scenarios where multiple clients want to generate meeting rooms. Eliminates the need to register multiple apps.
