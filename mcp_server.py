import sys
import json
import feedparser


def search_news(query):
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    feed = feedparser.parse(url)

    results = []
    query_terms = query.lower().split()

    for entry in feed.entries:
        text = (entry.title + " " + entry.get("summary", "")).lower()

        # Match ANY query term (robust filtering)
        if any(term in text for term in query_terms):
            results.append({
                "title": entry.title,
                "source": entry.source.title if "source" in entry else "Google News",
                "url": entry.link
            })

        if len(results) == 5:
            break

    return results


for line in sys.stdin:
    try:
        request = json.loads(line)

        if request.get("jsonrpc") != "2.0":
            raise ValueError("Invalid JSON-RPC version")

        if request.get("method") != "search":
            raise ValueError("Unsupported method")

        query = request["params"].get("query")
        if not query:
            raise ValueError("Missing query")

        results = search_news(query)

        if not results:
            response = {
                "jsonrpc": "2.0",
                "id": request["id"],
                "error": {
                    "code": -32001,
                    "message": "No news found"
                }
            }
        else:
            response = {
                "jsonrpc": "2.0",
                "id": request["id"],
                "result": results
            }

        print(json.dumps(response))
        sys.stdout.flush()

    except Exception as e:
        print(json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {
                "code": -32000,
                "message": str(e)
            }
        }))
        sys.stdout.flush()
