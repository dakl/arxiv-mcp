# arxiv-mcp

An [MCP](https://modelcontextprotocol.io/) server that exposes arXiv paper search, full-text HTML retrieval, and PDF download as tools. Built with [FastMCP](https://github.com/jlowin/fastmcp) and served over SSE.

## Tools

| Tool | Description |
|---|---|
| `search_papers` | Search arXiv for papers matching a query. Returns titles, authors, abstracts, and links. |
| `get_paper_html` | Retrieve the full text of an arXiv paper as HTML via [ar5iv](https://ar5iv.org). |
| `download_pdf` | Download an arXiv paper as PDF to a specified directory. |

## Quickstart

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run arxiv-mcp
```

The server starts on `http://0.0.0.0:8613`.

### Docker

```bash
docker compose up --build
```

## MCP client configuration

Add the server to your MCP client config:

```json
{
  "mcpServers": {
    "arxiv": {
      "url": "http://localhost:8613/sse"
    }
  }
}
```

## Development

```bash
uv sync                  # Install dependencies (including dev)
uv run pytest            # Run tests
uv run ruff check        # Lint
uv run ruff format       # Format
uv run pyright           # Type check
```

## Architecture

```
src/arxiv_mcp/
  domain.py   - Pydantic models (Paper)
  client.py   - arXiv API wrapper (search, HTML via ar5iv, PDF download)
  server.py   - FastMCP server exposing the three tools
```
