# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What is this?

An MCP (Model Context Protocol) server that exposes arXiv paper search, full-text HTML retrieval (via ar5iv), and PDF download as tools. Built with FastMCP and served over SSE on port 8613.

## Commands

```bash
uv sync                          # Install dependencies
uv run arxiv-mcp                 # Run the server (SSE on 0.0.0.0:8613)
uv run pytest                    # Run all tests
uv run pytest tests/test_client.py::test_extract_paper_id  # Run a single test
uv run ruff check                # Lint
uv run ruff format               # Format
uv run pyright                   # Type check (strict mode)
```

## Architecture

```
src/arxiv_mcp/
  domain.py   - Pydantic models (Paper)
  client.py   - arXiv API wrapper (search via `arxiv` lib, HTML via ar5iv, PDF download via httpx)
  server.py   - FastMCP server exposing three tools: search_papers, get_paper_html, download_pdf
```

The server is the entrypoint (`arxiv-mcp` script → `server:main`). It delegates all arXiv interaction to `client.py`, which builds `Paper` domain objects. The `search` function is synchronous (uses the `arxiv` library's blocking client); `get_html` and `download_pdf` are async (use `httpx.AsyncClient`).

## Conventions

- Python 3.13+, strict pyright, ruff line-length 100
- Pydantic BaseModel for all domain objects in `domain.py`
- Type hints on everything; avoid `Any`
- Package managed with uv (never pip)
- Docker: `docker compose up --build` to run containerized
