CREATE OR REPLACE TABLE `b2b_leads_dw.stg_b2b_leads` (
  company_name STRING OPTIONS(description="Company name extracted from web scraper"),
  company_website STRING OPTIONS(description="Company website domain or URL"),
  company_industry STRING OPTIONS(description="Industry or business sector"),
  target_role STRING OPTIONS(description="Title of the mapped decision-maker"),
  contact_email STRING OPTIONS(description="Enriched corporate contact email"),
  ingested_at TIMESTAMP OPTIONS(description="Timestamp when the record was ingested")
)
OPTIONS(
  description="Staging table for B2B leads ingested via n8n automation pipeline"
);