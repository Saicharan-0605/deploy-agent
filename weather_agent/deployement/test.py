# # This is the script you run locally to test your agent.
import time
from vertexai import agent_engines
import requests
import json
from collections import defaultdict
import traceback





def query_the_agent(user_id:str,agent_path:str,query:str,session_id:str=None):
    """Sends a single query to the deployed agent to generate a log entry."""
    try:
        agent = agent_engines.get(agent_path)
        if not session_id:
            session_id=agent.create_session(user_id=user_id)["id"]
        events = agent.stream_query(user_id="sai",session_id=session_id,message=query)
        events=list(events)
        payload=dict(session_id=session_id,agent_path=agent_path,events=events,user_id=user_id)
        response=requests.post(url="https://logging-for-db-444262030114.us-central1.run.app",json=payload)
        print(f"Status Code: {response.status_code}")
        try:
            response_data = response.json()
        except requests.exceptions.JSONDecodeError:
            response_data = response.text
        print(response_data)

    except Exception as e:
        print("Exception occured as ",e)



        

if __name__ == "__main__":
    messages=["tell me a joke","tell me about usa","will it rain in new york today"]
    for mes in messages:
        query_the_agent("sai","projects/444262030114/locations/us-central1/reasoningEngines/8759756361933258752",query="hi",session_id="5744618951397081088")