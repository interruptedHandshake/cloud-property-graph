# Test Case: Article 19 - Notification Obligation - Same Personal Data, Different Location
- Test case description: A user is registered in the "client_signup" page and his personal data is sent to a server. The server processes the data, saves it in a Mongo database and communicates parts of the personal data to a third party (external advertising server). On another page ("client_edit") the user can request deletion and rectification of his personal data, which was initially stored via signup. The server performs these requests and notifies the external advertising server about the deletion and rectification of the personal data. 
- Expected outcome:
  - No data flow is detected which does not fulfill the code properties of GDPR article 19.