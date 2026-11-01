CREATE OR REPLACE VIEW `b2b_leads_dw.dim_companies`
OPTIONS(
  description="Dimensional view of companies deduplicated by website domain, containing registration metadata and the date of initial ingestion."
) AS
SELECT
  TO_HEX(MD5(LOWER(TRIM(company_website)))) AS company_id,
  company_name,
  company_website,
  company_industry,
  MIN(ingested_at) AS created_at
FROM `b2b_leads_dw.stg_b2b_leads`
WHERE company_website IS NOT NULL
GROUP BY company_name, company_website, company_industry;

DROP TABLE IF EXISTS `b2b_leads_dw.dim_decision_makers`;

CREATE OR REPLACE VIEW `b2b_leads_dw.dim_decision_makers`
OPTIONS(
  description="A multidimensional view of B2B contacts and decision-makers, deduplicated by corporate email."
) AS
SELECT
  TO_HEX(MD5(LOWER(TRIM(contact_email)))) AS decision_maker_id,
  contact_email,
  target_role,
  MIN(ingested_at) AS created_at
FROM `b2b_leads_dw.stg_b2b_leads`
WHERE contact_email IS NOT NULL
GROUP BY contact_email, target_role;

DROP TABLE IF EXISTS `b2b_leads_dw.fct_leads_enrichment`;

CREATE OR REPLACE VIEW `b2b_leads_dw.fct_leads_enrichment`
OPTIONS(
  description="Fact table that records each lead ingestion event and calculates the contact enrichment rate."
) AS
SELECT
  TO_HEX(MD5(CONCAT(company_website, contact_email, CAST(ingested_at AS STRING)))) AS enrichment_id,
  TO_HEX(MD5(LOWER(TRIM(company_website)))) AS company_id,
  TO_HEX(MD5(LOWER(TRIM(contact_email)))) AS decision_maker_id,
  ingested_at,
  IF(contact_email IS NOT NULL AND target_role IS NOT NULL, 1, 0) AS is_enriched
FROM `b2b_leads_dw.stg_b2b_leads`;