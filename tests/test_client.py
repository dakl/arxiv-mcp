from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from arxiv_mcp.client import extract_paper_id, search


def test_extract_paper_id() -> None:
    assert extract_paper_id("http://arxiv.org/abs/2301.07041v1") == "2301.07041"
    assert extract_paper_id("http://arxiv.org/abs/2301.07041v3") == "2301.07041"
    assert extract_paper_id("http://arxiv.org/abs/hep-th/9901001v2") == "hep-th/9901001"


def _make_mock_result(entry_id: str, title: str, author_name: str) -> MagicMock:
    result = MagicMock()
    result.entry_id = entry_id
    result.title = title
    result.summary = "Some abstract"
    result.published = datetime(2023, 1, 17, tzinfo=timezone.utc)
    author = MagicMock()
    author.name = author_name
    result.authors = [author]
    return result


@patch("arxiv_mcp.client.arxiv")
def test_search_returns_papers(mock_arxiv: MagicMock) -> None:
    mock_client = MagicMock()
    mock_arxiv.Client.return_value = mock_client
    mock_client.results.return_value = [
        _make_mock_result("http://arxiv.org/abs/2301.07041v1", "Paper One", "Alice"),
    ]

    papers = search("test query", max_results=1)

    assert len(papers) == 1
    assert papers[0].paper_id == "2301.07041"
    assert papers[0].title == "Paper One"
    assert papers[0].authors == ["Alice"]
