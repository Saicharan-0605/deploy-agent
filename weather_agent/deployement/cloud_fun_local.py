import json
from collections import defaultdict
import traceback
from google.cloud.sql.connector import Connector, IPTypes
# import functions_framework
import datetime
import os
import pg8000
import sqlalchemy
from sqlalchemy import text
from vertexai import agent_engines


#to run the agent
PROJECT_ID = "deploy-agent-462707"
LOCATION = "us-central1"
AGENT_ID = "projects/deploy-agent-462707/locations/us-central1/reasoningEngines/927855872447610880"
USER_ID = "sai"

#for db connection
INSTANCE_CONNECTION_NAME = "deploy-agent-462707:us-central1:agent-with-db"
DB_USER = "postgres"
DB_PASS = "zolo"
DB_NAME = "eval"
IP_TYPE = IPTypes.PUBLIC  # Change to PRIVATE if you're using private IP
ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """
    Initializes a connection pool for a Cloud SQL instance of Postgres.

    Uses the Cloud SQL Python Connector package.
    """
    connector = Connector()

    def getconn() -> pg8000.dbapi.Connection:
        conn: pg8000.dbapi.Connection = connector.connect(
            INSTANCE_CONNECTION_NAME,
            "pg8000",
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME,
            ip_type=IP_TYPE,
        )
        return conn

    # The Cloud SQL Python Connector can be used with SQLAlchemy
    # using the 'creator' argument to 'create_engine'
    pool = sqlalchemy.create_engine(
        "postgresql+pg8000://",
        creator=getconn,
        # ...
    )
    return pool

def insert_logs_to_db(logs_to_insert):
        pool =connect_with_connector()
       
        # --- MODIFICATION 1: Add latency_seconds to the query ---
        insert_query = """
            INSERT INTO conversation_logs (
                session_id, user_id, invocation_id, conversation_turn,
                input_tokens, output_tokens, latency_seconds
            ) VALUES (
                :session_id, :user_id, :invocation_id, :conversation_turn,
                :input_tokens, :output_tokens, :latency_seconds
            ) ON CONFLICT (invocation_id) DO NOTHING;
        """
        with pool.connect() as db_conn:
            for log in logs_to_insert:
                print("inserting log")
                db_conn.execute(text(insert_query), log)
                db_conn.commit()
        # print(logs_to_insert)
        print(f"Successfully inserted/updated  log entries.")
        