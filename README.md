# Agent Skill Search Kit

Minimal no-key, citation-first search toolkit for coding agents. This starter exposes a small CLI that returns normalized JSON results from local demo providers and includes cache-friendly structure for real adapters.

## Install

```bash
python -m pip install -e .
```

## Usage

```bash
agent-skill-search search "agent skills" --provider demo
agent-skill-search export "wechat search" --format markdown
```

Output schema:

```json
{
  "query": "agent skills",
  "results": [
    {"title": "...", "url": "...", "source": "demo", "date": null, "snippet": "...", "citations": ["..."]}
  ]
}
```

## Development

```bash
python -m pip install -e .[dev]
pytest
```

## Next steps

- Add providers for Sogou/WeChat, GitHub, docs, packages, and generic web snippets.
- Add SQLite caching and provider rate-limit backoff.
- Ship AGENTS.md/CLAUDE.md prompt templates for agent workflows.
