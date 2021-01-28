"# GenerateTeamsMeetingRooms" 


We will be using MS Graph API.

Work Flow

Web Client needs to a meeting room -> Client calls our App -> We call MS Graph Create Events APUI -> pass Meeting details to client at API endpoint.

#USE CASE
For scenarios where calling msgraph directly is not feasible--within a large organization where security makes it difficult to gain necessary permissions, or any scenario where multiple clients want to generate meeting rooms, eliminates the need to register multiple apps.
