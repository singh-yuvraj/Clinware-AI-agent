from google import genai
from google.genai import types
from google.genai.errors import ClientError
from mcp_client import McpClient
from prompts import SYSTEM_PROMPT
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)
mcp = McpClient()


def needs_news(query: str) -> bool:
    keywords = ["news", "latest", "funding", "update", "happening", "launch", "working"]
    return any(k in query.lower() for k in keywords)


def run_agent():
    print("\nClinware Intelligence Agent")
    print("Ask about company news, funding, products, or general information:\n")

    tools = [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="search_company_news",
                    description="Search verified Google News via MCP",
                    parameters={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        },
                        "required": ["query"]
                    }
                )
            ]
        )
    ]

    while True:
        user_query = input("> ").strip()
        if user_query.lower() in ("exit", "quit"):
            break

        if needs_news(user_query):
            try:
                decision = client.models.generate_content(
                    model="models/gemini-flash-latest",
                    contents=f"""
Extract the main entity (company, product, or organization) from this query.
Return ONLY the name.

Query: {user_query}
""",
                    config=types.GenerateContentConfig(temperature=0.0)
                )
            except ClientError as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                    print("[Agent]: API usage limit reached. Please try again later.\n")
                else:
                    print("[Agent]: AI service error occurred.\n")
                continue

            entity = decision.text.strip() if decision.text else None

            if not entity:
                print("[Agent]: I need more context to identify what you want to search.\n")
                continue

            print(f"Agent calling search-news with keyword: {entity}")

            try:
                mcp_response = mcp.search(entity)
            except TimeoutError:
                print("[Agent]: MCP Server timeout. Please try again.\n")
                continue

            if "error" in mcp_response:
                print("[Agent]: No verified recent news found from Google News.\n")
                continue

            grounded_prompt = f"""
You are a market intelligence researcher.

Rules:
- Use ONLY the news below
- Do NOT add external knowledge
- Do NOT speculate

Summarize clearly and concisely.

News:
{mcp_response["result"]}
"""

            try:
                final = client.models.generate_content(
                    model="models/gemini-flash-latest",
                    contents=grounded_prompt,
                    config=types.GenerateContentConfig(temperature=0.0)
                )
            except ClientError as e:
                if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                    print("[Agent]: API usage limit reached. Please try again later.\n")
                else:
                    print("[Agent]: AI service error occurred.\n")
                continue

            if final.text:
                print(f"[Agent]: {final.text.strip()}")
                print("Source: Google News\n")
            else:
                print("[Agent]: Unable to summarize the retrieved news.\n")

            continue


        try:
            response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.0
                )
            )
        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e) or "quota" in str(e).lower():
                print("[Agent]: API usage limit reached. Please try again later.\n")
            else:
                print("[Agent]: AI service error occurred.\n")
            continue

        if response.text:
            print(f"[Agent]: {response.text.strip()}\n")
        else:
            print(
                "[Agent]: I couldn’t find enough reliable information. "
                "Could you please clarify what exactly you want to know?\n"
            )


if __name__ == "__main__":
    run_agent()
