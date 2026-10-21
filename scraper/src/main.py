import asyncio
import httpx
from models import CompanyLead
from bs4 import BeautifulSoup

async def fetch_html(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text

async def main():
    target_url = "https://httpbin.org/html"
    print(f"Fetching HTML from: {target_url}...")

    try:
        html_content = await fetch_html(target_url)

        soup = BeautifulSoup(html_content, "html.parser")

        titulo = soup.find('h1').get_text().strip()
        paragrafo = soup.find('p').get_text().strip()

        lead = CompanyLead(
            name=titulo, 
            website=target_url, 
            industry="Literature", 
            description=paragrafo
        )
        print("Objeto Pydantic Final:")
        print(lead.model_dump())

    except httpx.HTTPError as exc:
        print(f"HTTP error occurred: {exc}")


if __name__ == "__main__":
    asyncio.run(main())

