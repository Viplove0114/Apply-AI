"""
job_fetcher.py — Robust multi-strategy scraper for LinkedIn posts & job pages.

Strategies (tried in order):
  1. Direct GET with realistic browser headers
  2. JSON-LD structured data extraction
  3. OpenGraph / meta tag extraction
  4. Full HTML body text extraction as last resort

Works for LinkedIn posts, job listings, and most public career pages.
"""

import re
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# ── Realistic browser headers ────────────────────────────────
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Cache-Control": "no-cache",
    "Pragma": "no-cache",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "Referer": "https://www.google.com/",
}


def _is_linkedin_url(url: str) -> bool:
    """Check whether the URL belongs to LinkedIn."""
    domain = urlparse(url).netloc.lower()
    return "linkedin.com" in domain


def _fetch_html(url: str) -> BeautifulSoup:
    """
    Fetch a URL and return a BeautifulSoup object.
    Uses a requests.Session for cookie persistence.
    """
    session = requests.Session()
    session.headers.update(_HEADERS)

    # For LinkedIn, hit the homepage first to get cookies
    if _is_linkedin_url(url):
        try:
            session.get("https://www.linkedin.com", timeout=10)
        except requests.RequestException:
            pass  # Non-critical — continue anyway

    response = session.get(url, timeout=15, allow_redirects=True)
    response.raise_for_status()

    return BeautifulSoup(response.text, "lxml")


def _extract_json_ld(soup: BeautifulSoup) -> str | None:
    """
    Strategy: Extract text from JSON-LD structured data.
    LinkedIn and many job boards embed job details as JSON-LD.
    """
    scripts = soup.find_all("script", type="application/ld+json")
    for script in scripts:
        try:
            data = json.loads(script.string or "")

            # Handle list of JSON-LD items
            if isinstance(data, list):
                data = data[0] if data else {}

            # JobPosting schema
            if data.get("@type") == "JobPosting":
                parts = []
                if data.get("title"):
                    parts.append(f"Job Title: {data['title']}")
                if data.get("hiringOrganization", {}).get("name"):
                    parts.append(f"Company: {data['hiringOrganization']['name']}")
                if data.get("jobLocation"):
                    loc = data["jobLocation"]
                    if isinstance(loc, dict):
                        addr = loc.get("address", {})
                        loc_str = ", ".join(
                            filter(None, [
                                addr.get("addressLocality"),
                                addr.get("addressRegion"),
                                addr.get("addressCountry"),
                            ])
                        )
                        if loc_str:
                            parts.append(f"Location: {loc_str}")
                if data.get("description"):
                    # Description may contain HTML
                    desc_soup = BeautifulSoup(data["description"], "lxml")
                    parts.append(f"\n{desc_soup.get_text(separator='\n', strip=True)}")
                if parts:
                    return "\n".join(parts)

            # Article / SocialMediaPosting (LinkedIn posts)
            if data.get("@type") in ("Article", "SocialMediaPosting"):
                body = data.get("articleBody") or data.get("text") or ""
                if body:
                    return body

            # Generic: try description field
            if data.get("description"):
                return data["description"]

        except (json.JSONDecodeError, TypeError, KeyError):
            continue

    return None


def _extract_meta_tags(soup: BeautifulSoup) -> str | None:
    """
    Strategy: Extract content from OpenGraph and standard meta tags.
    LinkedIn always renders og:description even for logged-out users.
    """
    candidates = []

    # OpenGraph description (most reliable for LinkedIn)
    og_desc = soup.find("meta", property="og:description")
    if og_desc and og_desc.get("content"):
        candidates.append(og_desc["content"].strip())

    # Twitter card description
    tw_desc = soup.find("meta", attrs={"name": "twitter:description"})
    if tw_desc and tw_desc.get("content"):
        candidates.append(tw_desc["content"].strip())

    # Standard meta description
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc and meta_desc.get("content"):
        candidates.append(meta_desc["content"].strip())

    # OpenGraph title
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()
    else:
        title = ""

    if not candidates:
        return None

    # Use the longest candidate (usually has the most detail)
    best = max(candidates, key=len)

    # Combine title + description if title adds context
    if title and title not in best:
        return f"{title}\n\n{best}"
    return best


def _extract_body_text(soup: BeautifulSoup) -> str | None:
    """
    Strategy: Last resort — extract all visible text from the page body.
    Removes script, style, nav, footer, and header elements first.
    """
    # Remove non-content elements
    for tag in soup.find_all(["script", "style", "nav", "footer", "header", "noscript", "iframe"]):
        tag.decompose()

    # Try LinkedIn-specific content containers first
    content_selectors = [
        {"class_": re.compile(r"feed-shared-update-v2__description")},
        {"class_": re.compile(r"show-more-less-html__markup")},
        {"class_": re.compile(r"description__text")},
        {"class_": re.compile(r"core-section-container")},
        {"class_": re.compile(r"post-content")},
    ]

    for selector in content_selectors:
        container = soup.find("div", **selector)
        if container:
            text = container.get_text(separator="\n", strip=True)
            if len(text) > 50:  # Meaningful content threshold
                return text

    # Generic body extraction
    body = soup.find("body")
    if body:
        text = body.get_text(separator="\n", strip=True)
        # Clean up excessive whitespace
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        text = "\n".join(lines)
        if len(text) > 100:
            return text

    return None


def fetch_from_url(url: str) -> str:
    """
    Fetch job description / post content from a URL.
    Uses multiple strategies for robust extraction.

    Args:
        url: The URL to scrape (LinkedIn post, job listing, etc.)

    Returns:
        Extracted text content.

    Raises:
        ValueError: If no meaningful content could be extracted.
    """
    # Basic URL validation
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(
            "Invalid URL. Please provide a full URL starting with https://."
        )

    try:
        soup = _fetch_html(url)
    except requests.RequestException as e:
        raise ValueError(
            f"Could not reach the URL: {e}\n\n"
            "Please check the URL and your internet connection. "
            "If it's a private LinkedIn post, paste the job description manually."
        ) from e

    # Strategy 1: JSON-LD structured data
    result = _extract_json_ld(soup)
    if result and len(result) > 50:
        return result

    # Strategy 2: Meta tags (OpenGraph, Twitter, standard)
    result = _extract_meta_tags(soup)
    if result and len(result) > 50:
        return result

    # Strategy 3: Body text extraction
    result = _extract_body_text(soup)
    if result and len(result) > 50:
        return result

    raise ValueError(
        "Could not extract meaningful content from this URL.\n\n"
        "This may happen if:\n"
        "• The post is private or requires login\n"
        "• The page uses heavy JavaScript rendering\n\n"
        "Please paste the job description text manually instead."
    )
