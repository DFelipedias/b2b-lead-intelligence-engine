import os
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.cloud import bigquery
from google.oauth2 import service_account

app = FastAPI(title="B2B Lead Engine - Ingestion API")

class LeadPayload(BaseModel):
    company_name: str
    company_website: str
    company_industry: str
    target_role: str
    contact_email: str

def load_lead_to_bigquery(lead_dict: dict, credentials_path: str, project_id: str):
    credentials = service_account.Credentials.from_service_account_file(credentials_path)
    client = bigquery.Client(credentials=credentials, project=project_id)

    table_ref = client.dataset("b2b_leads_dw").table("stg_b2b_leads")
    
    record = lead_dict.copy()
    record["ingested_at"] = datetime.now(timezone.utc).isoformat()

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND
    )

    load_job = client.load_table_from_json(
        json_rows=[record],
        destination=table_ref,
        job_config=job_config
    )
    load_job.result()

@app.post("/api/v1/load-lead")
async def receive_lead_from_n8n(lead: LeadPayload):
    CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "gcp_key.json")
    PROJECT_ID = os.getenv("GCP_PROJECT_ID", "b2b-lead-engine-513001")

    try:
        lead_dict = lead.model_dump()
        load_lead_to_bigquery(lead_dict, CREDENTIALS_PATH, PROJECT_ID)
        return {"status": "success", "message": "Lead carregado no BigQuery com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))