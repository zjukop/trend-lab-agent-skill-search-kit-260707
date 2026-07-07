import json

from agent_skill_search_kit.main import main, search, to_markdown


def test_search_returns_normalized_results():
    response = search("agent skills", provider="github", limit=2)

    assert response.query == "agent skills"
    assert len(response.results) == 2
    assert response.results[0].title
    assert response.results[0].url.startswith("https://")
    assert response.results[0].citations


def test_markdown_export_contains_links():
    response = search("wechat", limit=1)

    markdown = to_markdown(response)

    assert "# Search results" in markdown
    assert "](https://" in markdown


def test_cli_outputs_json(capsys):
    exit_code = main(["search", "agent skills", "--limit", "1"])

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert exit_code == 0
    assert data["query"] == "agent skills"
    assert len(data["results"]) == 1
