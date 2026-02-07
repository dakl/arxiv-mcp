import argparse

from mcp.server.fastmcp import FastMCP

from arxiv_mcp import client
from arxiv_mcp.domain import Paper

DEFAULT_PORT = 8613

mcp = FastMCP("arxiv", host="0.0.0.0", port=DEFAULT_PORT)


@mcp.tool()
def search_papers(query: str, max_results: int = 10) -> list[Paper]:
    """Search arXiv for papers matching a query. Returns titles, authors, abstracts, and links."""
    return client.search(query, max_results)


@mcp.tool()
async def get_paper_html(paper_id: str) -> str:
    """Retrieve the full text of an arXiv paper as HTML (via ar5iv). Example paper_id: '2301.07041'."""
    return await client.get_html(paper_id)


@mcp.tool()
async def download_pdf(paper_id: str, output_dir: str = "./downloads") -> str:
    """Download an arXiv paper as PDF. Returns the path to the saved file."""
    path = await client.download_pdf(paper_id, output_dir)
    return str(path)


def main() -> None:
    parser = argparse.ArgumentParser(description="arxiv MCP server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"Port to listen on (default: {DEFAULT_PORT})")
    args = parser.parse_args()
    mcp.settings.port = args.port
    mcp.run(transport="sse")


if __name__ == "__main__":
    main()
