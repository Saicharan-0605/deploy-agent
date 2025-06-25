import pandas as pd
import psycopg2
import uuid
import json

DB_HOST = "aifabric-dev.cfccg2ksel4c.eu-north-1.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "docai"
DB_USER = "postgres"
DB_PASSWORD = "pAeg74a4N1sJkyFJjtVq"
 


def insert_into_db(metrices):
    unique_id = str(uuid.uuid4())

    json_metrics = json.dumps(metrices)

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    

    try:
        with conn:
            with conn.cursor() as cur:
                query = """
                    INSERT INTO conversation_metrics (id, metrics)
                    VALUES (%s, %s)
                """
                cur.execute(query, (unique_id, json_metrics))
                print("Inserted:", unique_id)
    except Exception as e:
        print("Error inserting:", e)
    finally:
        conn.close()
