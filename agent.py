from google import genai
from google.genai import types
from google.genai.errors import ClientError

from mcp_client import McpClient
from config import GEMINI_API_KEY
from prompts import NEWS_SUMMARIZATION_PROMPT



client = genai.Client(api_key=GEMINI_API_KEY)
mcp = McpClient()

MODEL = "models/gemini-flash-latest"



def safe_gemini_call(prompt: str) -> str | None:
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(temperature=0.0)
        )
        return response.text.strip() if response.text else None
    except ClientError as e:
        msg = str(e).lower()
        if "quota" in msg or "resource_exhausted" in msg:
            print("[Agent]: Gemini API quota exhausted.\n")
        else:
            print("[Agent]: Gemini API error.\n")
        return None




def generate_search_phrase(user_query: str) -> str | None:
    prompt = f"""
You are preparing a search query for Google News RSS.

Task:
Identify the MAIN SUBJECT that news articles would be written about.

STRICT RULES:
- Output ONLY the subject or entity name
- Do NOT include intent words (funding, founder, news, update, etc.)
- Do NOT include verbs or questions
- Do NOT include explanations
- The output must be a standalone RSS search term

User question:
"{user_query}"
"""
    return safe_gemini_call(prompt)




def summarize_news(news_data: list, user_query: str) -> str | None:
    prompt = NEWS_SUMMARIZATION_PROMPT.format(
        user_query=user_query,
        news_data=news_data
    )
    return safe_gemini_call(prompt)




def run_agent():
    print("\nClinware Intelligence Agent ")
    print("Facts come only from Google News RSS via MCP.")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("> ").strip()
        if user_query.lower() in ("exit", "quit"):
            break

    
        search_phrase = generate_search_phrase(user_query)

        if not search_phrase:
            print("[Agent]: Unable to identify subject for news search.\n")
            continue

        print(f"Agent calling search-news with query: {search_phrase}")

        try:
            mcp_response = mcp.search(search_phrase)
        except TimeoutError:
            print("[Agent]: MCP Server timeout.\n")
            continue

        if "error" in mcp_response:
            print("[Agent]: No verified recent news found.\n")
            continue

        summary = summarize_news(mcp_response["result"], user_query)

        if summary:
            print(f"[Agent]: {summary}")
            print("Source: Google News\n")
        else:
            print("[Agent]: The available news does not answer this question.\n")


if __name__ == "__main__":
    run_agent()
