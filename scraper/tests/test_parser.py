import pytest
from pathlib import Path
from pydantic import ValidationError
import sys

sys.path.append(str(Path(__file__).parent.parent / "src"))

from models import CompanyLead
from main import parse_leads_batch


def test_company_lead_valid_data():
    lead = CompanyLead(
        name="TechCorp",
        website="https://techcorp.com",
        industry="SaaS",
        description="Great B2B product",
    )
    assert lead.name == "TechCorp"
    assert lead.description == "Great B2B product"


def test_company_lead_optional_description():
    lead = CompanyLead(
        name="OpenData",
        website="https://opendata.org",
        industry="Data",
        description=None,
    )
    assert lead.description is None


def test_company_lead_missing_required_fields():

    with pytest.raises(ValidationError):
        CompanyLead(name="NoWebsiteCorp", industry="Tech") 


def test_parse_leads_batch_with_real_catalog():
    catalog_path = Path(__file__).parent.parent / "src" / "b2b_catalog.html"
    html_content = catalog_path.read_text(encoding="utf-8")

    leads = parse_leads_batch(html_content, source_url="https://directory.internal/b2b")

    assert len(leads) == 5

    first_lead = leads[0]
    assert first_lead.name == "Snowflake"
    assert first_lead.website == "https://snowflake.com"
    assert first_lead.industry == "Data Cloud"

    retool_lead = next(l for l in leads if l.name == "Retool")
    assert retool_lead.website == "https://retool.com"
    assert retool_lead.description is None


def test_parse_leads_batch_ignores_invalid_cards():
    broken_html = """
    <main>
        <!-- Card Válido -->
        <article class="company-card">
            <h2 class="company-title">ValidCo</h2>
            <a class="website-link" href="https://valid.com">Site</a>
            <span class="industry-badge">Fintech</span>
        </article>
        <!-- Card Quebrado (Sem link de site) -->
        <article class="company-card">
            <h2 class="company-title">BrokenCo</h2>
        </article>
    </main>
    """
    leads = parse_leads_batch(broken_html, source_url="https://test.local")

    assert len(leads) == 1
    assert leads[0].name == "ValidCo"