import json
from datetime import datetime, timedelta, timezone
from google.cloud import trace_v1
from google.api_core import exceptions
\
PROJECT_ID = "deploy-agent-462707"
OUTPUT_FILENAME = "spans.json"
client = trace_v1.TraceServiceClient()
end_time = datetime.now(timezone.utc)
start_time = end_time - timedelta(days=1)

request = {
    "project_id": PROJECT_ID,
    "start_time": start_time,
    "end_time": end_time,
    "view": trace_v1.ListTracesRequest.ViewType.COMPLETE
}
traces_pager = client.list_traces(request=request)

all_spans = []
for trace in traces_pager:
    for span in trace.spans:
        all_spans.append({
            "trace_id": trace.trace_id,
            "project_id": trace.project_id,
            "span_id": span.span_id,
            "name": span.name,
            "start_time": span.start_time.isoformat(),
            "end_time": span.end_time.isoformat(),
            "labels": dict(span.labels)
        })

with open(OUTPUT_FILENAME, "w", encoding="utf-8") as f:
        json.dump(all_spans, f, indent=2, ensure_ascii=False)
