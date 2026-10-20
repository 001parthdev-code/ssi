# SSI — System Security Investigator

V0: **Query → Investigate → Report**.

## Zero-cost local setup (Windows PowerShell)

Requires Python 3.10+, Ollama installed and running, and internet access for search.

```powershell
ollama pull qwen3.5:4b
python -m pip install -e ".[free]"
python -m ssi.cli "What financial losses have been caused by AI in finance?" --depth normal --output report.json
```

The CLI uses **DuckDuckGo search + local Ollama by default**. No paid API credentials are required. Use `--model YOUR_OLLAMA_MODEL` or set `SSI_OLLAMA_MODEL` to select a different installed model. Ollama's local endpoint defaults to `http://127.0.0.1:11434`.

The report is saved to `report.json` and contains query, depth, summary, findings, sources and limitations. This is a prototype: it only analyzes **search result snippets**, not full pages, and must not be treated as a verified incident report. Unofficial DuckDuckGo search can rate-limit or fail. The model may still make mistakes; check citations manually.

Depth currently controls number of search results (normal 5, medium 10, extreme 20), not autonomous research iterations.

## Optional paid providers

```powershell
python -m pip install -e ".[live]"
$env:BRAVE_SEARCH_API_KEY="..."
$env:OPENAI_API_KEY="..."
python -m ssi.cli "Your query" --provider cloud
```

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Next milestone

Add safe full-document retrieval, evidence attribution and iterative investigation. Do not expose Ollama or the SSI backend directly to the public internet.
