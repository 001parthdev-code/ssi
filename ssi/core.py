"""Investigation pipeline: query -> source discovery -> evidence -> report."""
from dataclasses import dataclass, asdict
from typing import Protocol
import json

@dataclass(frozen=True)
class Source:
    title: str
    url: str
    snippet: str

@dataclass(frozen=True)
class Report:
    query: str
    depth: str
    summary: str
    findings: list[str]
    sources: list[Source]
    limitations: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)

class SearchProvider(Protocol):
    def search(self, query: str, limit: int) -> list[Source]: ...

class Analyzer(Protocol):
    def analyze(self, query: str, sources: list[Source]) -> tuple[str, list[str], list[str]]: ...

DEPTH_LIMITS = {"normal": 5, "medium": 10, "extreme": 20}

def investigate(query: str, depth: str, search: SearchProvider, analyzer: Analyzer) -> Report:
    query = query.strip()
    if not query or len(query) > 2000:
        raise ValueError("Query must be between 1 and 2000 characters")
    if depth not in DEPTH_LIMITS:
        raise ValueError("Depth must be normal, medium, or extreme")
    sources = search.search(query, DEPTH_LIMITS[depth])
    # Deduplicate by URL; never manufacture sources.
    sources = list({s.url: s for s in sources if s.url.startswith(("https://", "http://"))}.values())
    if not sources:
        return Report(query, depth, "No sources were retrieved.", [], [], ["No evidence available; no conclusions drawn."])
    summary, findings, limitations = analyzer.analyze(query, sources)
    return Report(query, depth, summary, findings, sources, limitations)
