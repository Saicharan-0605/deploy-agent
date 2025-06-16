# This is the script you run locally to test your agent.

import time
from vertexai import agent_engines
from google.cloud import logging
from google.api_core import exceptions

# --- Configuration for YOUR AGENT ---
PROJECT_ID = "444262030114"  # The project number where the agent is deployed
LOCATION = "us-central1"
REASONING_ENGINE_ID = "927855872447610880" # The ID of your deployed agent

# --- Configuration for YOUR LOGS ---
# This LOG_ID must EXACTLY match the LOG_NAME defined in agent_main.py
LOG_ID_TO_FETCH = "reasoning_engine_activity" 

# --- The Workflow ---

def query_the_agent():
    """Sends a single query to the deployed agent to generate a log entry."""
    print("--- STEP 1: Sending query to the agent ---")
    try:
        agent= agent_engines.get('projects/444262030114/locations/us-central1/reasoningEngines/927855872447610880')
        quer=agent.stream_query(user_id="sai",message="how is weather in new york?")
        for item in quer:
            print(item)
        print(f"Agent responded successfully. A log should now exist.\n")

    except Exception as e:
        print(f"ERROR: Failed to query the agent. {e}")
        print("Please check your agent ID, permissions, and ensure the agent is deployed.\n")
        return False
    return True

def fetch_the_logs():
    """Fetches and prints recent logs from the agent."""
    print("--- STEP 2: Fetching recent logs from Cloud Logging ---")
    try:
        logging_client = logging.Client(project="444262030114") # Project where logs are stored
        
        # Build a filter to get ONLY the logs from your specific agent.
        filter_str = (
            f'logName="projects/444262030114/logs/{LOG_ID_TO_FETCH}" '
            f'AND resource.labels.reasoning_engine_id="{REASONING_ENGINE_ID}"'
        )
        print(f"Using filter: {filter_str}")

        # Fetch the log entries
        log_entries = logging_client.list_entries(filter_=filter_str,order_by=logging.DESCENDING, page_size=5)
        
        print("\n--- Most Recent Logs ---")
        entry_found = False
        for entry in log_entries:
            entry_found = True
            timestamp = entry.timestamp.isoformat()
            payload = entry.payload
            print(f"* Timestamp: {timestamp}")
            print(f"  Payload: {payload}\n")
        
        if not entry_found:
            print("No matching log entries found.")

    except exceptions.PermissionDenied:
        print("ERROR: Permission Denied. Ensure you have the 'Logs Viewer' role for project 'deploy-agent-462707'.")
    except Exception as e:
        print(f"An unexpected error occurred while fetching logs: {e}")

# --- Main Execution ---
if __name__ == "__main__":
    # if query_the_agent():
    #     # Give Cloud Logging a few seconds to ingest the new log entry.
    #     print("Waiting 5 seconds for logs to be ingested...")
    #     time.sleep(5)
    fetch_the_logs()