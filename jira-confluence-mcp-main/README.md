# Confluence MCP Server

Python-based MCP (Model Context Protocol) server for interacting with Atlassian Confluence API.

## Setup

### 1. Install Dependencies

```bash
uv sync
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and set your credentials:

```bash
cp .env.example .env
```

Set the following environment variables:
- `CONFLUENCE_URL`: Your Confluence instance URL
- `CONFLUENCE_USERNAME`: Your email address
- `CONFLUENCE_API_TOKEN`: API token (generate at [Atlassian Account Settings](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/))
- `CONFLUENCE_CLOUD`: Set to `true` for cloud instances, `false` for server instances

## Usage

### Start Confluence MCP Server

```bash
uv run python src/confluence_server.py
```

## Available Tools

- `confluence_search_content`: Search for content using CQL query
- `confluence_get_page`: Get page details by ID
- `confluence_create_page`: Create a new page
- `confluence_update_page`: Update an existing page
- `confluence_delete_page`: Delete a page
- `confluence_get_spaces`: Get list of spaces
- `confluence_get_page_children`: Get child pages
- `confluence_add_attachment`: Add attachment to a page

## Claude Desktop Configuration

Add the following to your Claude Desktop config file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "confluence": {
      "command": "/path/to/confluence-mcp/run_confluence.sh",
      "args": [],
      "env": {
        "CONFLUENCE_URL": "https://your-domain.atlassian.net",
        "CONFLUENCE_USERNAME": "your-email@example.com",
        "CONFLUENCE_API_TOKEN": "your-api-token",
        "CONFLUENCE_CLOUD": "true"
      }
    }
  }
}
```

**Note**: 
- Replace `/path/to/confluence-mcp/` with the actual project path
- Generate API token at [Atlassian Account Settings](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)
- `run_confluence.sh` is located in the project root

### Jira

```python
# イシューの検索
await jira_search_issues({"jql": "project = PROJ AND status = 'In Progress'", "max_results": 10})

# イシューの作成
await jira_create_issue({
    "project_key": "PROJ",
    "summary": "新しいタスク",
    "description": "タスクの説明",
    "issue_type": "Task",
    "priority": "Medium"
})

# イシューのステータス変更
await jira_transition_issue({"issue_key": "PROJ-123", "status": "Done"})
```

### Confluence

```python
# ページの検索
await confluence_search_content({"cql": "space = DEV AND title ~ 'API'"})

# ページの作成
await confluence_create_page({
    "space_key": "DEV",
    "title": "新しいドキュメント",
    "content": "<p>ページの内容</p>"
})

# ページの更新
await confluence_update_page({
    "page_id": "123456",
    "content": "<p>更新された内容</p>",
    "version_comment": "APIドキュメントを更新"
})
```

## ライセンス

MIT
