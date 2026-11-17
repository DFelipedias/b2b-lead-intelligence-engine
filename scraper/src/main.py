import asyncio
import httpx
from bs4 import BeautifulSoup
from models import CompanyLead


async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def parse_leads_batch(html_content: str, source_url: str) -> list[CompanyLead]:
    soup = BeautifulSoup(html_content, "html.parser")
    validated_leads = []

    cards = soup.find_all("article", class_="company-card")
    for card in cards:
    
        title_elem = card.find("h2", class_="company-title")
        link_elem = card.find("a", class_="website-link")
        industry_elem = card.find("span", class_="industry-badge")
        desc_elem = card.find("p", class_="description")
        
        company_name = title_elem.get_text(strip=True) if title_elem else None
        website = link_elem.get("href") if link_elem else None
        industry = industry_elem.get_text(strip=True) if industry_elem else "General Tech"
        description = desc_elem.get_text(strip=True) if desc_elem else None
        
        if company_name and website:
            try:
                lead = CompanyLead(
                    name=company_name,
                    website=website,
                    industry=industry,
                    description=description,
                )
                validated_leads.append(lead)
            except Exception as e:
                print(f"Error to validate lead {company_name}: {e}")

    return validated_leads


async def send_to_webhook(webhook_url: str, payload: list[dict]) -> None:
    async with httpx.AsyncClient() as client:
        print(f"Dispatching batch of {len(payload)} lead(s) to webhook...")
        response = await client.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Webhook dispatch success! Status code: {response.status_code}")


async def main():
    target_url = "https://httpbin.org/html"
    
    webhook_test_url = "http://host.docker.internal:5678/webhook-test/b2b-leads-ingestion"

    print(f"Starting batch extraction from: {target_url}...\n")

    try:
      
        html_content = await fetch_html(target_url)

        leads_objects = parse_leads_batch(html_content, target_url)

        payload_batch = [lead.model_dump() for lead in leads_objects]

        if payload_batch:
            await send_to_webhook(webhook_test_url, payload_batch)

    except httpx.HTTPError as exc:
        print(f"HTTP error occurred during execution: {exc}")

if __name__ == "__main__":
    asyncio.run(main())