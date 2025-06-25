import pandas as pd
 
import vertexai
from vertexai.evaluation import EvalTask, PointwiseMetric, PointwiseMetricPromptTemplate
from google.cloud import aiplatform
 
PROJECT_ID = "deploy-agent-462707"
LOCATION = "us-central1"
STAGING_BUCKET = "gs://deploy-agent123"
EXPERIMENT_NAME = "evaluation"
# --- Initialize Vertex AI SDK ---
vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
)
 
# --- Existing Metric: Analyst Response Quality (Unchanged) ---
custom_analyst_evaluation = PointwiseMetric(
    metric="analyst_response_quality",
    metric_prompt_template=PointwiseMetricPromptTemplate(
        criteria={
            "accuracy": (
                "The response correctly reflects the source data, factual content, "
                "and logical conclusions based on the query. No incorrect statements are made."
            ),
            "hallucination": (
                "The response avoids including information that is not grounded in the provided input "
                "or data. It should not fabricate facts or make unverifiable claims."
            ),
        },
        rating_rubric={
            "1": "The response is accurate and free from hallucinations.",
            "0": "The response is somewhat accurate but contains minor hallucinations or unverified content.",
            "-1": "The response is inaccurate and/or contains significant hallucinations.",
        },
    ),
)
 
# --- NEW: Metric for Sentiment Analysis ---
sentiment_evaluation = PointwiseMetric(
    metric="sentiment_analysis",
    metric_prompt_template=PointwiseMetricPromptTemplate(
        criteria={
            "sentiment": (
                "Assess the sentiment of the response. A positive sentiment might express success, growth, or good news. "
                "A negative sentiment might express loss, decline, or bad news. "
                "A neutral sentiment presents facts without an emotional or biased tone."
            )
        },
        rating_rubric={
            "1": "The response has a positive sentiment (e.g., expresses growth, success).",
            "0": "The response has a neutral sentiment (e.g., states a fact without emotion).",
            "-1": "The response has a negative sentiment (e.g., expresses decline, loss).",
        },
    ),
)
 
 
# --- Dataset ---
responses = [
    "The revenue for Q1 2024 was $3.5 million, showing a 12 percent increase from Q4 2023, as reported in the company’s financial statement.",
    "The company likely earned over $5 million in Q1 based on trends, even though the exact number isn't stated.",
    "The company partnered with NASA in Q1 2024 to launch a financial satellite, boosting earnings to $10 million.",
]
 
eval_dataset = pd.DataFrame({
    "response": responses,
})
 
# --- Evaluation Task Definition (Updated) ---
# We add the new sentiment_evaluation metric to the list.
eval_task = EvalTask(
    dataset=eval_dataset,
    metrics=[custom_analyst_evaluation, sentiment_evaluation], # ADDED sentiment_evaluation
    experiment=EXPERIMENT_NAME
)
 
# --- Run Evaluation ---
pointwise_result = eval_task.evaluate()
 
# --- Print Results ---
# The output table will now have columns for both metrics.
print(pointwise_result.metrics_table)