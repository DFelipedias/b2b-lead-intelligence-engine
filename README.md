# 🚀 B2B Lead Intelligence Engine - Data Ingestion Layer

An asynchronous, containerized data ingestion pipeline engineered to extract, validate, and structure B2B company data from public web directories.

## 🏗️ Architecture & Pipeline Overview

This microservice forms the **Ingestion Layer (STG)** of an end-to-end Analytics Engineering pipeline:

[ Target Web Source ]
│
▼ (Async HTTP GET via httpx)
[ Scraper Engine (Docker / Python 3.11) ]
│
▼ (HTML Parsing via BeautifulSoup4)
[ Schema Validation (Pydantic v2) ]
│
▼ (Validated JSON Payload / Dict Batch)
[ Downstream Enrichment (n8n Webhook / BigQuery)

## 🛠️ Tech Stack & Engineering Decisions

* **Language:** Python 3.11 (Asyncio)
* **Data Validation:** Pydantic v2 (Strict Schema Contracts)
* **Networking & Parsing:** HTTPx (Non-blocking I/O), BeautifulSoup4
* **Containerization:** Docker (Isolated Environment)

## 🔑 Key Features

* **Resilient Data Contract:** Handles optional fields gracefully using Pydantic `Optional[T]` types to prevent runtime pipeline crashes on missing web element attributes.
* **Non-Blocking Architecture:** Built on top of `httpx.AsyncClient` and `asyncio` Event Loop for scalable web throughput.
* **Production-Ready Containerization:** Dockerized microservice ensuring 100% environment reproducibility across staging and production.

## 🚀 Quick Start (Local Execution)

Ensure you have **Docker Desktop** installed and running.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/DFelipedias/b2b-lead-intelligence-engine.git](https://github.com/DFelipedias/b2b-lead-intelligence-engine.git)
   cd b2b-lead-intelligence-engine