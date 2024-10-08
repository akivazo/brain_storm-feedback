GET /

Description: Root endpoint that returns a message "Feedback Api" to verify the service is running.
Response:
200: "Feedback Api"

POST /feedback

Description: Adds a new feedback entry for an idea. The feedback data (including idea_id, owner_id, and content) is passed in the request body. A unique id is generated for the feedback, and it is stored in the feedbacks array under the corresponding idea_id. If idea_id doesn't exist, a new document is created.
Request Body (JSON):
idea_id: ID of the idea.
owner_id: ID of the owner of the feedback.
content: Feedback content.
Response:
201: Returns the newly generated id of the feedback.
400: Returns an error message if validation fails.

GET /feedbacks/<idea_id>

Description: Retrieves all feedbacks for a specific idea. The idea_id is passed as a URL parameter. Returns all feedbacks associated with the idea_id.
URL Parameter:
idea_id: ID of the idea to fetch feedback for.
Response:
302: Returns the list of feedbacks for the given idea_id.
404: Returns an error message if no feedbacks are found for the specified idea_id.

DELETE /feedback/<idea_id>/<feedback_id>

Description: Deletes a specific feedback from an idea. The idea_id and feedback_id are passed as URL parameters. Removes the feedback with the specified feedback_id from the feedbacks array of the corresponding idea.
URL Parameters:
idea_id: ID of the idea containing the feedback.
feedback_id: ID of the feedback to be deleted.
Response:
204: No content, indicating successful deletion.

DELETE /feedbacks/<idea_id>

Description: Deletes all feedbacks for a specific idea. The idea_id is passed as a URL parameter. The entire document containing the idea_id and its associated feedbacks is removed.
URL Parameter:
idea_id: ID of the idea for which all feedbacks should be deleted.
Response:
204: No content, indicating successful deletion of the idea and its feedbacks.