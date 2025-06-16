# This is the code for your agent that runs on GCP.

import os
import json
import logging
from typing import Dict
import google.cloud.logging

print("Attempting to configure Google Cloud Logging for the agent...")

try:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        project_id = "deploy-agent-462707" 

    client = google.cloud.logging.Client(project=project_id)

    # *** BEST PRACTICE CHANGE ***
    # Let's give our log stream a specific, clear name.
    # This is the LOG_ID you were asking about. We are defining it here.
    LOG_NAME = "reasoning_engine_activity"

    resource = google.cloud.logging.Resource(
        type="aiplatform.googleapis.com/ReasoningEngine",
        labels={
            "project_id": project_id,
            "location": os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
            "reasoning_engine_id": os.environ.get("GOOGLE_CLOUD_AGENT_ENGINE_ID", "local-dev-or-import"),
        },
    )

    # Set up the handler to use our specific log name.
    handler = client.get_default_handler(name=LOG_NAME)
    handler.resource = resource
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    print(f"Successfully configured Google Cloud Logging to write to '{LOG_NAME}'.")

except Exception as e:
    print(f"CRITICAL: Failed to configure Cloud Logging. Error: {e}")


class MyAgent:
    """The agent logic that gets deployed."""
    def set_up(self):
        logging.info("MyAgent.set_up() called.")
        pass

    def query(self, input: Dict) -> Dict:
        logging.info({"event": "request_received", "input_data": input})
        try:
            # Your agent's logic here...
            user_query = input.get("message", "No message provided.")
            response_payload = {"status": "success", "message": f"Processed query: '{user_query}'"}
            logging.info({"event": "response_sent", "output_data": response_payload})
            return response_payload
        except Exception as e:
            logging.error({"event": "error_occurred", "error_message": str(e)})
            return {"status": "error", "message": "An internal error occurred."}