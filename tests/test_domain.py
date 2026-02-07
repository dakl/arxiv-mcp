from datetime import datetime, timezone

from arxiv_mcp.domain import Paper


def test_paper_roundtrip() -> None:
    paper = Paper(
        paper_id="2301.07041",
        title="Test Paper",
        authors=["Alice", "Bob"],
        abstract="An abstract.",
        published=datetime(2023, 1, 17, tzinfo=timezone.utc),
        pdf_url="https://arxiv.org/pdf/2301.07041",
        html_url="https://ar5iv.org/html/2301.07041",
    )
    data = paper.model_dump()
    restored = Paper.model_validate(data)
    assert restored == paper


def test_paper_json_serialization() -> None:
    paper = Paper(
        paper_id="2301.07041",
        title="Test Paper",
        authors=["Alice"],
        abstract="Abstract text.",
        published=datetime(2023, 1, 17, tzinfo=timezone.utc),
        pdf_url="https://arxiv.org/pdf/2301.07041",
        html_url="https://ar5iv.org/html/2301.07041",
    )
    json_str = paper.model_dump_json()
    restored = Paper.model_validate_json(json_str)
    assert restored == paper
