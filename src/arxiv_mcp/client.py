from pathlib import Path

import arxiv
import httpx

from arxiv_mcp.domain import Paper

_AR5IV_BASE = "https://ar5iv.org/html"
_ARXIV_PDF_BASE = "https://arxiv.org/pdf"


def extract_paper_id(entry_id: str) -> str:
    return entry_id.rsplit("/abs/", maxsplit=1)[-1].split("v")[0]


def search(query: str, max_results: int = 10) -> list[Paper]:
    client = arxiv.Client()
    results = client.results(arxiv.Search(query=query, max_results=max_results))
    papers: list[Paper] = []
    for r in results:
        paper_id = extract_paper_id(r.entry_id)
        papers.append(
            Paper(
                paper_id=paper_id,
                title=r.title,
                authors=[a.name for a in r.authors],
                abstract=r.summary,
                published=r.published,
                pdf_url=f"{_ARXIV_PDF_BASE}/{paper_id}",
                html_url=f"{_AR5IV_BASE}/{paper_id}",
            )
        )
    return papers


async def get_html(paper_id: str) -> str:
    url = f"{_AR5IV_BASE}/{paper_id}"
    async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


async def download_pdf(paper_id: str, output_dir: str = ".") -> Path:
    url = f"{_ARXIV_PDF_BASE}/{paper_id}"
    dest = Path(output_dir) / f"{paper_id}.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
        async with client.stream("GET", url) as response:
            response.raise_for_status()
            with dest.open("wb") as f:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    f.write(chunk)
    return dest
