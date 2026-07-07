from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import date
from typing import Literal


@dataclass(frozen=True)
class SearchResult:
    title: str
    url: str
    source: str
    date: str | None
    snippet: str
    citations: list[str]


@dataclass(frozen=True)
class SearchResponse:
    query: str
    provider: str
    results: list[SearchResult]


def search(query: str, provider: str = "demo", limit: int = 5) -> SearchResponse:
    """Return normalized search results.

    This starter uses deterministic demo data so tests and agent workflows are runnable
    without API keys or network access. Replace this with provider adapters.
    """
    if limit < 1:
        raise ValueError("limit must be >= 1")

    sources = {
        "demo": "https://example.com/search",
        "wechat": "https://weixin.sogou.com/",
        "github": "https://github.com/search",
        "docs": "https://docs.python.org/3/",
    }
    base_url = sources.get(provider, sources["demo"])
    results = [
        SearchResult(
            title=f"{query} result {i}",
            url=f"{base_url}?q={query.replace(' ', '+')}&n={i}",
            source=provider,
            date=date.today().isoformat(),
            snippet=f"Citation-first snippet for {query} from {provider}.",
            citations=[base_url],
        )
        for i in range(1, limit + 1)
    ]
    return SearchResponse(query=query, provider=provider, results=results)


def to_markdown(response: SearchResponse) -> str:
    lines = [f"# Search results for `{response.query}`", ""]
    for item in response.results:
        lines.append(f"- [{item.title}]({item.url}) — {item.snippet} Source: {item.source}")
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent-friendly structured search CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("search", "export"):
        cmd = sub.add_parser(name)
        cmd.add_argument("query")
        cmd.add_argument("--provider", default="demo")
        cmd.add_argument("--limit", type=int, default=5)
        if name == "export":
            cmd.add_argument("--format", choices=["json", "markdown"], default="json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    response = search(args.query, args.provider, args.limit)

    if args.command == "export" and args.format == "markdown":
        print(to_markdown(response), end="")
    else:
        print(json.dumps(asdict(response), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
