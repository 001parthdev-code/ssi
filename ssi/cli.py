"""CLI entrypoint."""
import argparse
from pathlib import Path
from .core import investigate


def main() -> None:
    parser = argparse.ArgumentParser(description="SSI security investigation")
    parser.add_argument("query", help="Security research question")
    parser.add_argument("--depth", choices=["normal", "medium", "extreme"], default="normal")
    parser.add_argument("--provider", choices=["free", "cloud"], default="free")
    parser.add_argument("--model", help="Ollama model tag (free provider only)")
    parser.add_argument("--output", default="report.json")
    args = parser.parse_args()
    if args.provider == "free":
        from .free_providers import DuckDuckGoSearch, OllamaAnalyzer
        search, analyzer = DuckDuckGoSearch(), OllamaAnalyzer(model=args.model)
    else:
        if args.model:
            parser.error("--model is only supported for the free provider")
        from .providers import BraveSearch, OpenAIAnalyzer
        search, analyzer = BraveSearch(), OpenAIAnalyzer()
    report = investigate(args.query, args.depth, search, analyzer)
    path = Path(args.output)
    path.write_text(report.to_json() + "\n", encoding="utf-8")
    print(f"Report written to {path}")


if __name__ == "__main__":
    main()
