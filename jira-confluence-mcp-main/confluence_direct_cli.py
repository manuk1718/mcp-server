#!/usr/bin/env python3
import argparse
import json
import os
from typing import Any

from atlassian import Confluence
from dotenv import load_dotenv


def _json_print(data: Any) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=True))


def _get_confluence_client() -> Confluence:
    project_env = os.path.join(os.path.dirname(__file__), ".env")
    load_dotenv(dotenv_path=project_env)

    url = os.getenv("CONFLUENCE_URL", "")
    username = os.getenv("CONFLUENCE_USERNAME", "")
    api_token = os.getenv("CONFLUENCE_API_TOKEN", "")
    cloud = os.getenv("CONFLUENCE_CLOUD", "true").lower() == "true"

    if not all([url, username, api_token]):
        raise ValueError(
            "Missing env vars. Set CONFLUENCE_URL, CONFLUENCE_USERNAME, and CONFLUENCE_API_TOKEN."
        )

    return Confluence(
        url=url,
        username=username,
        password=api_token,
        cloud=cloud,
    )


def cmd_list_spaces(client: Confluence, args: argparse.Namespace) -> None:
    spaces = client.get_all_spaces(limit=args.limit)
    _json_print(spaces.get("results", []))


def cmd_search(client: Confluence, args: argparse.Namespace) -> None:
    results = client.cql(args.cql, limit=args.limit)
    _json_print(results.get("results", []))


def cmd_get_page(client: Confluence, args: argparse.Namespace) -> None:
    page = client.get_page_by_id(args.page_id, expand=args.expand)
    _json_print(page)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Direct Confluence CLI (no MCP client needed)."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_list_spaces = subparsers.add_parser("list-spaces", help="List Confluence spaces")
    p_list_spaces.add_argument("--limit", type=int, default=25)
    p_list_spaces.set_defaults(func=cmd_list_spaces)

    p_search = subparsers.add_parser("search", help="Search content with CQL")
    p_search.add_argument("--cql", required=True, help="CQL query")
    p_search.add_argument("--limit", type=int, default=25)
    p_search.set_defaults(func=cmd_search)

    p_get_page = subparsers.add_parser("get-page", help="Get page by ID")
    p_get_page.add_argument("--page-id", required=True, help="Confluence page ID")
    p_get_page.add_argument("--expand", default="body.storage,version", help="Expand fields")
    p_get_page.set_defaults(func=cmd_get_page)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    client = _get_confluence_client()
    args.func(client, args)


if __name__ == "__main__":
    main()
