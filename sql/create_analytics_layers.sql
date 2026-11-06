CREATE OR REPLACE VIEW `b2b_leads_dw.dim_time` 
OPTIONS(description="Time dimension (Calendar) for temporal analysis in BI.") AS
WITH dates AS (
  SELECT date_array 
  FROM UNNEST(GENERATE_DATE_ARRAY('2024-01-01', '2030-12-31', INTERVAL 1 DAY)) AS date_array
)
SELECT 
  CAST(FORMAT_DATE('%Y%m%d', date_array) AS INT64) AS sk_time, -- Key: 20240101
  date_array AS full_date,
  EXTRACT(YEAR FROM date_array) AS year,
  EXTRACT(QUARTER FROM date_array) AS quarter,
  EXTRACT(MONTH FROM date_array) AS month,
  FORMAT_DATE('%B', date_array) AS month_name,
  EXTRACT(DAY FROM date_array) AS day,
  EXTRACT(DAYOFWEEK FROM date_array) AS day_of_week
FROM dates;

CREATE OR REPLACE VIEW `b2b_leads_dw.dim_companies`
OPTIONS(
  description="Dimensional view of companies deduplicated by website domain, containing registration metadata and the date of initial ingestion."
) AS
SELECT
  TO_HEX(MD5(LOWER(TRIM(company_website)))) AS company_id,
  company_name,
  company_website,
  company_industry,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', MIN(ingested_at)) AS INT64) AS sk_time, -- inserido a sk tempo
  MIN(ingested_at) AS created_at
FROM `b2b_leads_dw.stg_b2b_leads`
WHERE company_website IS NOT NULL
GROUP BY company_name, company_website, company_industry;

CREATE OR REPLACE VIEW `b2b_leads_dw.dim_decision_makers`
OPTIONS(
  description="A multidimensional view of B2B contacts and decision-makers, deduplicated by corporate email."
) AS
SELECT
  TO_HEX(MD5(LOWER(TRIM(contact_email)))) AS decision_maker_id,
  contact_email,
  target_role,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', MIN(ingested_at)) AS INT64) AS sk_time, -- inserido a sk
  MIN(ingested_at) AS created_at
FROM `b2b_leads_dw.stg_b2b_leads`
WHERE contact_email IS NOT NULL
GROUP BY contact_email, target_role;

CREATE OR REPLACE VIEW `b2b_leads_dw.fct_leads_enrichment`
OPTIONS(
  description="Fact table that records each lead ingestion event and calculates the contact enrichment rate."
) AS
SELECT
  TO_HEX(MD5(CONCAT(company_website, contact_email, CAST(ingested_at AS STRING)))) AS enrichment_id,
  TO_HEX(MD5(LOWER(TRIM(company_website)))) AS company_id,
  TO_HEX(MD5(LOWER(TRIM(contact_email)))) AS decision_maker_id,
  CAST(FORMAT_TIMESTAMP('%Y%m%d', ingested_at) AS INT64) AS sk_time, -- inserido a sk
  ingested_at,
  IF(contact_email IS NOT NULL AND target_role IS NOT NULL, 1, 0) AS is_enriched
FROM `b2b_leads_dw.stg_b2b_leads`;