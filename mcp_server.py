import json
import sys
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

def search_news(query):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_KEY
    }

    res = requests.get(url, params=params, timeout=10)
    data = res.json()

    articles = []
    for a in data.get("articles", [])[:5]:
        articles.append({
            "title": a["title"],
            "source": a["source"]["name"],
            "url": a["url"]
        })

    return articles


for line in sys.stdin:
    request = json.loads(line)

    if request["method"] == "search":
        result = search_news(request["params"]["query"])
        response = {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": result
        }
        print(json.dumps(response))
        sys.stdout.flush()