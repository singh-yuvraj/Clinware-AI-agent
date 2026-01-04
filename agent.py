import logging
from google import genai
from google.genai import types
from mcp_client import McpClient
from prompts import SYSTEM_PROMPT
from config import GEMINI_API_KEY


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


client = genai.Client(api_key=GEMINI_API_KEY)


mcp = McpClient()


def search_clinware_news(query: str):
    return mcp.search(query)


def run_agent():
    logging.info("Clinware Market Intelligence Agent started")

    user_query = input("Ask about Clinware: ")
    logging.info(f"User query received: {user_query}")


    tools = [
        types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="search_clinware_news",
                    description="Fetch latest Clinware news from MCP server",
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


    response = client.models.generate_content(
        model="models/gemini-flash-latest",
        contents=user_query,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            tools=tools
        )
    )


    for part in response.candidates[0].content.parts:
        if part.function_call:
            logging.info("Tool call detected: search_clinware_news")

            news = search_clinware_news(user_query)
            logging.info(f"News articles fetched: {len(news)}")

            if not news:
                logging.warning("No public news found for Clinware")

                print("\n=== Clinware Market Intelligence Summary ===\n")
                print(
                    "No recent public news related to Clinware was found at the time of analysis.\n"
                    "This may be due to limited media coverage or the company operating privately."
                )
                print("\nData Source: NewsAPI (via Local MCP Server)")
                return

            grounded_prompt = f"""
            Using ONLY the following news data, generate a market intelligence summary:

            {news}
            """

            final_response = client.models.generate_content(
                model="models/gemini-flash-latest",
                contents=grounded_prompt
            )

            print("\n=== Clinware Market Intelligence Summary ===\n")
            print(final_response.text)
            print("\nData Source: NewsAPI (via Local MCP Server)")
            print("Note: This summary is based solely on publicly available information.")
            return


    logging.info("No tool call required for this query")
    print(response.text)


if __name__ == "__main__":
    run_agent()
