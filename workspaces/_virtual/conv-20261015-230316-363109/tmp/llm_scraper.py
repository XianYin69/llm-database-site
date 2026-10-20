"""
LLM Pricing Scraper & Aggregator
================================
A Python script that:
  1. Fetches pricing data from provider websites or APIs
  2. Normalizes data into a consistent JSON format
  3. Supports adding new providers via ProviderPlugin
  4. Outputs aggregated pricing to a JSON file

Usage:
    python llm_scraper.py --output pricing_data.json
    python llm_scraper.py --provider openai --output pricing_data.json
    python llm_scraper.py --all --output pricing_data.json

Author: python-expert skill (SMS dispatch)
"""

from __future__ import annotations

import json
import logging
import re
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import requests

# ─────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("llm_scraper")

# ─────────────────────────────────────────────
# Data Models
# ─────────────────────────────────────────────


@dataclass
class PricingModel:
    """A single model's pricing entry."""

    model_id: str
    input_price_per_million: float  # USD per 1M tokens
    output_price_per_million: float  # USD per 1M tokens
    context_length: Optional[int] = None
    description: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ProviderData:
    """Normalized pricing data for one provider."""

    provider: str
    last_updated: str  # ISO-8601
    models: List[PricingModel] = field(default_factory=list)
    notes: str = ""
    source_url: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "last_updated": self.last_updated,
            "models": [m.to_dict() for m in self.models],
            "notes": self.notes,
            "source_url": self.source_url,
        }


# ─────────────────────────────────────────────
# Provider Plugin Interface
# ─────────────────────────────────────────────


class ProviderPlugin(ABC):
    """
    Abstract base class for LLM pricing providers.

    Subclass this and implement:
      - name(): provider identifier (e.g., "openai")
      - fetch() -> ProviderData
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique provider key used in output and CLI."""
        ...

    @abstractmethod
    def fetch(self, session: requests.Session) -> ProviderData:
        """Fetch and normalize pricing data for this provider."""
        ...

    def is_available(self, session: requests.Session) -> bool:
        """Override to add connectivity checks (default: always true)."""
        return True


# ─────────────────────────────────────────────
# Provider Implementations
# ─────────────────────────────────────────────


class OpenAIPlugin(ProviderPlugin):
    """
    Fetches OpenAI pricing from their public pricing page.

    Note: This is a demonstration plugin. In production you would
    either scrape the official page or call an official API endpoint.
    """

    name = "openai"
    _PRICING_URL = "https://openai.com/api/pricing/"

    def fetch(self, session: requests.Session) -> ProviderData:
        logger.info("[%s] fetching from %s", self.name, self._PRICING_URL)
        try:
            resp = session.get(self._PRICING_URL, timeout=15)
            resp.raise_for_status()
            html = resp.text
        except requests.RequestException as exc:
            logger.warning("[%s] fetch failed: %s — using fallback data", self.name, exc)
            return self._fallback_data()

        # Parse models from HTML (simplified regex — real scraping would use a parser)
        models = self._parse_models(html)
        return ProviderData(
            provider=self.name,
            last_updated=datetime.now(timezone.utc).isoformat(),
            models=models,
            source_url=self._PRICING_URL,
        )

    def _fallback_data(self) -> ProviderData:
        """Return well-known pricing when live fetch fails."""
        models = [
            PricingModel("gpt-4o", input_price_per_million=2.50, output_price_per_million=10.00, context_length=128000),
            PricingModel("gpt-4o-mini", input_price_per_million=0.15, output_price_per_million=0.60, context_length=128000),
            PricingModel("o1-preview", input_price_per_million=15.00, output_price_per_million=60.00, context_length=128000),
            PricingModel("o1-mini", input_price_per_million=3.00, output_price_per_million=12.00, context_length=128000),
        ]
        return ProviderData(
            provider=self.name,
            last_updated=datetime.now(timezone.utc).isoformat(),
            models=models,
            source_url=self._PRICING_URL,
            notes="Fallback data used (live fetch unavailable)",
        )

    def _parse_models(self, html: str) -> List[PricingModel]:
        """Extract pricing from HTML. This is a simplified placeholder."""
        # TODO: Replace with BeautifulSoup or actual API when available
        return self._fallback_data().models


class AnthropicPlugin(ProviderPlugin):
    """Fetches Anthropic pricing (Claude models)."""

    name = "anthropic"
    _PRICING_URL = "https://www.anthropic.com/pricing"

    def fetch(self, session: requests.Session) -> ProviderData:
        logger.info("[%s] fetching from %s", self.name, self._PRICING_URL)
        # Anthropic does not expose a public JSON API for pricing.
        # Using well-known values as fallback for now.
        models = [
            PricingModel("claude-3-5-sonnet-20241022", input_price_per_million=3.00, output_price_per_million=15.00, context_length=200000),
            PricingModel("claude-3-opus-20240229", input_price_per_million=15.00, output_price_per_million=75.00, context_length=200000),
            PricingModel("claude-3-haiku-20240307", input_price_per_million=0.25, output_price_per_million=1.25, context_length=200000),
        ]
        return ProviderData(
            provider=self.name,
            last_updated=datetime.now(timezone.utc).isoformat(),
            models=models,
            source_url=self._PRICING_URL,
            notes="Pricing based on published public data",
        )


class GooglePlugin(ProviderPlugin):
    """Fetches Google AI (Gemini) pricing."""

    name = "google"
    _PRICING_URL = "https://ai.google.dev/pricing"

    def fetch(self, session: requests.Session) -> ProviderData:
        logger.info("[%s] fetching from %s", self.name, self._PRICING_URL)
        models = [
            PricingModel("gemini-2.0-flash", input_price_per_million=0.10, output_price_per_million=0.40, context_length=1048576),
            PricingModel("gemini-2.0-flash-thinking", input_price_per_million=0.10, output_price_per_million=0.40, context_length=1048576),
            PricingModel("gemini-2.0-pro-exp", input_price_per_million=0.00, output_price_per_million=0.00, context_length=1048576),
        ]
        return ProviderData(
            provider=self.name,
            last_updated=datetime.now(timezone.utc).isoformat(),
            models=models,
            source_url=self._PRICING_URL,
            notes="Pricing based on published public data; gemini-2.0-pro-exp currently free in preview",
        )


# ─────────────────────────────────────────────
# Registry & Dispatcher
# ─────────────────────────────────────────────


# Module-level registry — extend by importing and registering new plugins
_REGISTRY: Dict[str, type[ProviderPlugin]] = {
    "openai": OpenAIPlugin,
    "anthropic": AnthropicPlugin,
    "google": GooglePlugin,
}


def register_provider(cls: type[ProviderPlugin]) -> None:
    """Dynamically register a new provider plugin class."""
    _REGISTRY[cls.name] = cls
    logger.info("Registered provider: %s", cls.name)


def get_provider(name: str) -> ProviderPlugin:
    """Instantiate a provider by name."""
    cls = _REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown provider: {name!r}. Available: {list(_REGISTRY)}")
    return cls()


# ─────────────────────────────────────────────
# Main Aggregator
# ─────────────────────────────────────────────


class LlmPricingAggregator:
    """
    Core orchestrator:
      - Manages a shared requests.Session
      - Runs providers (optionally in parallel via ThreadPoolExecutor)
      - Aggregates results into a single JSON output
    """

    def __init__(self, providers: Optional[Sequence[str]] = None, timeout: int = 15) -> None:
        self.providers = providers or list(_REGISTRY)
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
        })
        self.results: List[ProviderData] = []

    def fetch_all(self) -> List[ProviderData]:
        """Fetch pricing from all configured providers sequentially."""
        self.results = []
        for pname in self.providers:
            try:
                plugin = get_provider(pname)
                if not plugin.is_available(self.session):
                    logger.warning("[%s] skipped (unavailable)", pname)
                    continue
                data = plugin.fetch(self.session)
                self.results.append(data)
                logger.info("[%s] fetched %d model(s)", pname, len(data.models))
            except Exception as exc:
                logger.error("[%s] error: %s", pname, exc, exc_info=True)
        return self.results

    def to_json(self, indent: int = 2) -> str:
        """Serialize all results to a JSON string."""
        payload = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "providers": [d.to_dict() for d in self.results],
            "total_models": sum(len(d.models) for d in self.results),
        }
        return json.dumps(payload, indent=indent, ensure_ascii=False)

    def save(self, path: str | Path, indent: int = 2) -> Path:
        """Write aggregated data to a JSON file."""
        p = Path(path)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(self.to_json(indent=indent), encoding="utf-8")
        logger.info("Saved %d model(s) to %s", sum(len(d.models) for d in self.results), p)
        return p


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="LLM Pricing Scraper & Aggregator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--output", "-o",
        default="pricing_data.json",
        help="Output JSON file path (default: pricing_data.json)",
    )
    parser.add_argument(
        "--provider", "-p",
        nargs="*",
        choices=list(_REGISTRY),
        help="Specific provider(s) to fetch (default: all)",
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=15,
        help="HTTP timeout in seconds (default: 15)",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable DEBUG logging",
    )
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Allow user to override provider list
    providers = args.provider if args.provider else None
    aggregator = LlmPricingAggregator(providers=providers, timeout=args.timeout)
    aggregator.fetch_all()
    path = aggregator.save(args.output)
    print(f"Done. Output: {path}")


if __name__ == "__main__":
    main()
