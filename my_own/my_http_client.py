import asyncio
import os
from urllib.parse import urljoin

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


def build_candidate_urls() -> list[str]:
    explicit = os.getenv("MCP_SERVER_URL")
    if explicit:
        return [explicit]

    base = os.getenv("MCP_SERVER_BASE_URL", "http://127.0.0.1:8000/")
    if not base.endswith("/"):
        base += "/"

    # FastMCP examples commonly use /mcp; keep / as fallback.
    return [urljoin(base, "mcp"), base]


async def try_connect(url: str) -> bool:
    try:
        async with streamablehttp_client(url) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                tools = await session.list_tools()
                tool_names = [tool.name for tool in tools.tools]
                print(f"Connected via streamable-http at {url}. Tools: {tool_names}")
                return True
    except Exception as exc:
        print(f"Failed at {url}: {exc}")
        return False


async def main() -> None:
    for url in build_candidate_urls():
        if await try_connect(url):
            return

    raise RuntimeError(
        "Could not connect to MCP server over streamable-http. "
        "Set MCP_SERVER_URL to the exact endpoint."
    )


if __name__ == "__main__":
    asyncio.run(main())
