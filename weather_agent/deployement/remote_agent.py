from google import auth as google_auth
from google.auth.transport import requests as google_requests
import requests
import json

def get_identity_token():
    credentials, _ = google_auth.default()
    auth_request = google_requests.Request()
    credentials.refresh(auth_request)
    return credentials.token
requests.post(
    f"https://us-central1-aiplatform.googleapis.com/v1/projects/deploy-agent-462707/locations/us-central1/reasoningEngines/927855872447610880:streamQuery",
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {get_identity_token()}",
    },
    data=json.dumps({
        "class_method": "stream_query",
        "input": {
            "user_id": "sai",
            "session_id": "5037659363016179712",
            "message": "What is the exchange rate from US dollars to SEK today?",
        },
    }),
    stream=True,
)