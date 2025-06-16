# from typing import Dict

# class MyAgent:

#     def set_up(self):
#         import os
#         import google.cloud.logging

#         self.logging_client = google.cloud.logging.Client(project="deploy-agent-462707")
#         self.logging_client.setup_logging(
#             name="my_Agent",  # the ID of the logName in Cloud Logging.
#             resource=google.cloud.logging.Resource(
#                 type="aiplatform.googleapis.com/ReasoningEngine",
#                 labels={
#                     "location": "us-central1",
#                     "resource_container": "deploy-agent-462707",
#                     "reasoning_engine_id": os.environ.get("GOOGLE_CLOUD_AGENT_ENGINE_ID", "927855872447610880"),
#                 },
#             ),
#         )

#     def query(self, input: Dict):
#         import logging
#         import json

#         logging_extras = {
#             "labels": {"foo": "bar"},
#             "trace": "TRACE_ID",
#         }

#         logging.info( # or .warning(), .error()
#             json.dumps(input),
#             extra=logging_extras,
#         )


import vertexai

# PROJECT_ID = "deploy-agent-462707"
# LOCATION = "us-central1"
# STAGING_BUCKET = "gs://deploy-agent123"

# vertexai.init(
#     project=PROJECT_ID,
#     location=LOCATION,
#     staging_bucket=STAGING_BUCKET,
# )
# remote_agent = agent_engines.create(
#     MyAgent(),
#     requirements=["cloudpickle==3", "google-cloud-logging"],
# )

# from vertexai import agent_engines
# agent_engine = vertexai.agent_engines.get('projects/444262030114/locations/us-central1/reasoningEngines/3891787377210818560')

# resp=agent_engine.query(input={"hello": "world"})

# print(resp)


 