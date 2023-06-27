Credentials
Handles the credentials form submission.

URL: /creds

Parameters:

None

Returns:

If POST method:
Template: app/creds.html
Context:
access_token: Access token if authentication is successful
If other methods:
Template: app/creds.html
Execute Script
Executes a script on a specified host.

URL: /execute_script

Parameters:

None

Returns:

If POST method:
Template: app/execute_script.html
Generate Access Token
Generates an access token using the provided API key and secret.

Parameters:

api_key: API key
api_secret: API secret
Returns:

Access token if authentication is successful, None otherwise.
Main
Renders the main page.

URL: /main

Parameters:

None

Returns:

Template: app/main.html



