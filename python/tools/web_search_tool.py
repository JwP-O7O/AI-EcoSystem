from python.helpers.tool import Tool, Response
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote_plus

class WebSearch(Tool):
    async def execute(self, **kwargs):
        """
        Advanced web search tool with multiple search engines
        """
        self.agent.set_data("paused", True)

        query = kwargs.get("query", "")
        engine = kwargs.get("engine", "duckduckgo")  # duckduckgo, google, bing
        max_results = kwargs.get("max_results", 5)

        if not query:
            return Response(message="Please provide a search query", break_loop=False)

        self.log.log(type="info", heading=f"Web Search: {query}")

        try:
            results = []

            if engine == "duckduckgo":
                results = self._search_duckduckgo(query, max_results)
            elif engine == "google":
                results = self._search_google(query, max_results)
            elif engine == "bing":
                results = self._search_bing(query, max_results)

            formatted_results = self._format_results(results)

            message = self.agent.read_prompt(
                "tool.web_search.response.md",
                query=query,
                results=formatted_results
            )

            return Response(message=message, break_loop=False)

        except Exception as e:
            return Response(message=f"Search error: {str(e)}", break_loop=False)

    def _search_duckduckgo(self, query, max_results):
        """Search using DuckDuckGo"""
        url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for result in soup.find_all('div', class_='result')[:max_results]:
            title_elem = result.find('a', class_='result__a')
            snippet_elem = result.find('a', class_='result__snippet')

            if title_elem:
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'url': title_elem.get('href', ''),
                    'snippet': snippet_elem.get_text(strip=True) if snippet_elem else ''
                })

        return results

    def _search_google(self, query, max_results):
        """Search using Google (basic scraping)"""
        url = f"https://www.google.com/search?q={quote_plus(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for g in soup.find_all('div', class_='g')[:max_results]:
            title = g.find('h3')
            link = g.find('a')
            snippet = g.find('div', class_='VwiC3b')

            if title and link:
                results.append({
                    'title': title.get_text(strip=True),
                    'url': link.get('href', ''),
                    'snippet': snippet.get_text(strip=True) if snippet else ''
                })

        return results

    def _search_bing(self, query, max_results):
        """Search using Bing"""
        url = f"https://www.bing.com/search?q={quote_plus(query)}"
        headers = {'User-Agent': 'Mozilla/5.0'}

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        results = []
        for result in soup.find_all('li', class_='b_algo')[:max_results]:
            title = result.find('h2')
            link = result.find('a')
            snippet = result.find('p')

            if title and link:
                results.append({
                    'title': title.get_text(strip=True),
                    'url': link.get('href', ''),
                    'snippet': snippet.get_text(strip=True) if snippet else ''
                })

        return results

    def _format_results(self, results):
        """Format search results for display"""
        formatted = []
        for i, result in enumerate(results, 1):
            formatted.append(
                f"{i}. **{result['title']}**\n"
                f"   URL: {result['url']}\n"
                f"   {result['snippet']}\n"
            )
        return "\n".join(formatted)
