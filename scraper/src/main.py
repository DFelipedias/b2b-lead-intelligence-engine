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

    title_tag = soup.find("h1")
    paragraph_tag = soup.find("p")

    if title_tag:
        lead = CompanyLead(
            name=title_tag.get_text().strip(),
            website=source_url,
            industry="Literature",
            description=paragraph_tag.get_text().strip() if paragraph_tag else None,
        )
        validated_leads.append(lead)

    return validated_leads


async def send_to_webhook(webhook_url: str, payload: list[dict]) -> None:
    async with httpx.AsyncClient() as client:
        print(f"Dispatching batch of {len(payload)} lead(s) to webhook...")
        response = await client.post(webhook_url, json=payload)
        response.raise_for_status()
        print(f"Webhook dispatch success! Status code: {response.status_code}")


async def main():
    target_url = "https://httpbin.org/html"
    webhook_test_url = "https://httpbin.org/post"

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