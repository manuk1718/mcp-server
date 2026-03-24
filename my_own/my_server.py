from typing import Any, Optional
from mcp.server.fastmcp import FastMCP
from urllib.parse import quote
import httpx
import sys
import base64
import os
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("temp_file")

mcp.settings.port = int(os.getenv("PORT",8000))
CONFLUENCE_BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
USERNAME = os.getenv("USERNAME")
API_TOKEN = os.getenv("API_TOKEN")

# This function will return python object
# This funtion is used to connect confluence page, So every tool calls this
async def make_confluence_request(
	url: str, method: str = "GET", params: dict = None
) -> dict[str, Any] | str:
	auth_string = f"{USERNAME}:{API_TOKEN}"
	auth_bytes = auth_string.encode("ascii")
	base64_auth = base64.b64encode(auth_bytes).decode("ascii")
	headers = {"Authorization": f"Basic {base64_auth}", "Accept": "application/json"}

	async with httpx.AsyncClient() as client:
		try:
			if method == "GET":
				response = await client.get(url, headers=headers, params=params)
			else:
				response = await client.request(method, url, headers=headers, json=params)

			response.raise_for_status()
			return response.json()
		except httpx.HTTPError as e:
			return f"Error making request: {str(e)}"
		except Exception as e:
			return f"Unexpected error: {str(e)}"

@mcp.tool()
async def get_page_content(page_id: str) -> str:
	url = f"{CONFLUENCE_BASE_URL}rest/api/content/{page_id}"
	params = {"expand": "body.storage,version,space,metadata.labels"}

	data = await make_confluence_request(url, params=params)

	if isinstance(data, str):  # Error case
		return data

	title = data.get("title", "Unknown")
	space = data.get("space", {}).get("name", "Unknown")
	version = data.get("version", {}).get("number", "Unknown")
	content = data.get("body", {}).get("storage", {}).get("value", "No content")
	labels = [
		label.get("name")
		for label in data.get("metadata", {}).get("labels", {}).get("results", [])
	]
	return f"Title : {title} \n Content:{content}"

@mcp.tool()
async def search_content(query: str, limit: Optional[int] = 25) -> str:
	url = f"{CONFLUENCE_BASE_URL}rest/api/search"
	cql = f'text~"{query}"'
	params = {"cql": cql, "limit": limit}

	data = await make_confluence_request(url, params=params)

	if isinstance(data, str):  # Error case
		return data

	# Format the response
	result = []
	for content in data.get("results", []):
		content_info = f"""
 Title: {content.get('title', 'Unknown')}
 Type: {content.get('type', 'Unknown')}
 ID: {content.get('id', 'Unknown')}"""
		result.append(content_info)

	return "\n---\n".join(result) if result else "No results found"

if __name__ == "__main__":
	mcp.run()