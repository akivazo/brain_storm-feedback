from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from uuid import uuid4
from pydantic import BaseModel, ValidationError
from typing import Type

class FeedbackSchema(BaseModel):
    id: str
    idea_id: str
    owner_id: str
    content: str

server = Flask(__name__)
CORS(server)
collection = None

def set_mongo_client(mongo_client: MongoClient):
    global collection
    collection = mongo_client.get_database("brain_storm").get_collection("feedbacks")

@server.route("/")
def root():
    return "Feedback Api"

def validate_json_schema(json: dict, cls: Type):
    # validate that the accepted json is containing all the data nedded
    instance = None
    try:
        instance = cls(**json)
    except ValidationError as e:
        return None, e.json()
    return instance.__dict__, ""

@server.route("/feedback", methods=["POST"])
def add_feedback():
    data = request.get_json()
    id = str(uuid4())
    data["id"] = id
    feedback_dict, error_message = validate_json_schema(data, FeedbackSchema)
    if not feedback_dict:
        return jsonify({"error": error_message}), 400
    idea_id = feedback_dict["idea_id"]
    del feedback_dict["idea_id"]
    collection.update_one(
        {"idea_id": idea_id}, 
        {"$push": {"feedbacks": feedback_dict}},
        upsert=True)
    return jsonify({"id": id}), 201


@server.route("/feedbacks/<idea_id>", methods=["GET"])
def get_feedbacks(idea_id: str):
    feedbacks = collection.find_one({"idea_id": idea_id}, {"_id": 0, "feedbacks": 1})

    if feedbacks:
        return jsonify(feedbacks), 302
    return jsonify({"feedbacks": []}), 204

@server.route("/feedback/<idea_id>/<feedback_id>", methods=["DELETE"])
def delete_feedback(idea_id, feedback_id: str):
    collection.update_one({"idea_id": idea_id}, {"$pull": {"feedbacks": {"id": feedback_id}}})
    return "", 204

@server.route("/feedbacks/<idea_id>", methods=["DELETE"])
def delete_idea_feedbacks(idea_id: str):
    collection.delete_one({"idea_id": idea_id})
    return "", 204

if __name__ == "__main__":
    import os, dotenv
    dotenv.load_dotenv()
    mongo_client = MongoClient(os.environ["FEEDBACK_MONGODB_URI"])
    set_mongo_client(mongo_client)
    server.run(debug=True, port=5000)
    mongo_client.close()