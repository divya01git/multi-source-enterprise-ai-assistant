"""
Enterprise AI Assistant
Web Search Tool
"""

from __future__ import annotations

from typing import Any, Dict, List
from urllib.parse import urlparse

from ddgs import DDGS

from utils.config import MAX_WEB_RESULTS


class WebSearchTool:
    """
    Handles external web search using DuckDuckGo.

    Responsibilities:
    - Search the web
    - Remove duplicate results
    - Prefer authoritative sources
    - Prefer official and primary sources
    - Preserve source URLs
    - Return structured search results
    """

    # ---------------------------------------------------------
    # Trusted Domains
    # ---------------------------------------------------------

    TRUSTED_DOMAINS = {
        "github.com",
        "docs.github.com",
        "langchain.com",
        "python.langchain.com",
        "docs.langchain.com",
        "openai.com",
        "platform.openai.com",
        "developers.google.com",
        "learn.microsoft.com",
        "microsoft.com",
        "aws.amazon.com",
        "cloud.google.com",
        "arxiv.org",
        "research.google",
        "engineering.fb.com",
        "meta.com",
    }

    # ---------------------------------------------------------
    # Lower Priority Domains
    # ---------------------------------------------------------

    LOWER_PRIORITY_DOMAINS = {
        "dev.to",
        "linkedin.com",
        "medium.com",
        "quora.com",
    }

    # ---------------------------------------------------------
    # Initialization
    # ---------------------------------------------------------

    def __init__(self):

        pass

    # ---------------------------------------------------------
    # Domain Helpers
    # ---------------------------------------------------------

    @staticmethod
    def _get_domain(
        url: str,
    ) -> str:
        """
        Extracts the normalized domain from a URL.
        """

        try:

            hostname = urlparse(
                url
            ).hostname

            if not hostname:

                return ""

            hostname = hostname.lower()

            if hostname.startswith(
                "www."
            ):

                hostname = hostname[4:]

            return hostname

        except Exception:

            return ""

    @classmethod
    def _is_trusted_domain(
        cls,
        domain: str,
    ) -> bool:
        """
        Checks whether a domain is trusted or belongs
        to a trusted parent domain.
        """

        for trusted_domain in cls.TRUSTED_DOMAINS:

            if (
                domain == trusted_domain
                or domain.endswith(
                    "." + trusted_domain
                )
            ):

                return True

        return False

    @classmethod
    def _is_lower_priority_domain(
        cls,
        domain: str,
    ) -> bool:
        """
        Identifies sources that should receive lower
        priority when stronger sources are available.
        """

        for lower_domain in cls.LOWER_PRIORITY_DOMAINS:

            if (
                domain == lower_domain
                or domain.endswith(
                    "." + lower_domain
                )
            ):

                return True

        return False

    # ---------------------------------------------------------
    # Result Ranking
    # ---------------------------------------------------------

    @classmethod
    def _rank_result(
        cls,
        result: Dict[str, Any],
    ) -> int:
        """
        Assigns a source-quality score.

        Higher score = higher priority.
        """

        url = result.get(
            "url",
            "",
        )

        domain = cls._get_domain(
            url
        )

        score = 0

        # Official / primary sources
        if cls._is_trusted_domain(
            domain
        ):

            score += 100

        # Lower-priority opinion/blog platforms
        if cls._is_lower_priority_domain(
            domain
        ):

            score -= 30

        # Strong indicators of primary technical sources
        url_lower = url.lower()

        if any(
            keyword in url_lower
            for keyword in [
                "/releases",
                "/release",
                "/docs",
                "/documentation",
                "/changelog",
                "/blog",
                "/news",
                "/announcements",
            ]
        ):

            score += 20

        return score

    # ---------------------------------------------------------
    # Deduplicate Results
    # ---------------------------------------------------------

    @staticmethod
    def _deduplicate_results(
        results: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Removes duplicate URLs.
        """

        unique_results = []

        seen_urls = set()

        for result in results:

            url = (
                result.get(
                    "url",
                    "",
                )
                .strip()
                .lower()
            )

            if not url:

                continue

            if url in seen_urls:

                continue

            seen_urls.add(
                url
            )

            unique_results.append(
                result
            )

        return unique_results

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        query: str,
    ) -> List[Dict[str, Any]]:
        """
        Searches the web and returns ranked results.

        Results are prioritized toward:
        - Official documentation
        - Official repositories
        - Release pages
        - Primary technical sources

        Lower-authority sources are retained only when
        useful, but are ranked below stronger sources.
        """

        if not query or not query.strip():

            return []

        results = []

        try:

            with DDGS() as ddgs:

                search_results = ddgs.text(
                    query,
                    max_results=MAX_WEB_RESULTS,
                )

                for item in search_results:

                    title = (
                        item.get(
                            "title",
                            "",
                        )
                        or ""
                    ).strip()

                    content = (
                        item.get(
                            "body",
                            "",
                        )
                        or ""
                    ).strip()

                    url = (
                        item.get(
                            "href",
                            "",
                        )
                        or ""
                    ).strip()

                    if not url:

                        continue

                    results.append(
                        {
                            "title": title,
                            "content": content,
                            "url": url,
                        }
                    )

            results = self._deduplicate_results(
                results
            )

            results.sort(
                key=self._rank_result,
                reverse=True,
            )

            return results[
                :MAX_WEB_RESULTS
            ]

        except Exception as e:

            print(
                f"Web Tool Error: {e}"
            )

            return []


web_tool = WebSearchTool()