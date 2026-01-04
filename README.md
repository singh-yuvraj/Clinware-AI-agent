# Clinware-AI-agent

# Overview
The Clinware Market Intelligence Agent is a production-style AI research assistant designed to provide factually grounded market intelligence about companies, products, and organizations.



## The agent combines:


Google Gemini (LLM) for reasoning, intent detection, and summarization

A local MCP-compliant News Server

JSON-RPC–based client/server communication

Google News RSS as a verifiable public data source



## The key goal of this project is to demonstrate how to build an AI agent that:

Knows when to fetch real-world data

Uses tools responsibly

Never hallucinates news

Separates reasoning from data access


## Key Capabilities


### Intent-Aware Query Handling:

Automatically distinguishes between general knowledge and news-based questions

### Tool Calling with MCP:

Invokes a local MCP News Server when real-world news is required

### JSON-RPC Communication:

Client/server interaction over standard input/output using JSON-RPC 2.0

### Grounded AI Responses:
News summaries are generated only from MCP-provided data
No external assumptions or hallucinations

### Graceful Error Handling:
Handles:
No news found
MCP server timeouts
Always responds clearly and safely

Professional Research-Agent Behavior:
Asks for clarification when information is insufficient
Avoids speculative or biographical guesses

---




#  System Flow

1. The user submits a natural language query to the system.

2. The agent (agent.py) receives the query and acts as the central controller.

3. The agent analyzes the query to determine whether real-time news is required.

4. If news is required, the agent uses Gemini to extract the relevant entity.

5. The extracted entity is sent to the MCP client using JSON-RPC.

6. The MCP server retrieves verified public news from Google News RSS.

7. The agent injects the retrieved news into Gemini for grounded summarization.

8. If no news is required, Gemini generates a general informational response.

9. The final output is concise, factual, and free from hallucinations.


### The architecture ensures that all responses are grounded in real-time data fetched via an MCP-compliant server, preventing hallucinations.

---




# How It Works
===============
### 1. User Input

The user enters a natural language query, such as:

What is the latest news on Clinware funding?

### 2. Intent Detection

The agent checks for news-related keywords:

`news`

`latest`

`funding`

`update`

`happening`

`launch`

`working`

If detected → news flow
Otherwise → general knowledge flow

### 3. Entity Extraction (LLM Reasoning)

For news queries, Gemini is asked to:

Extract the primary entity (company, product, or organization).

This step:

Avoids hardcoded company lists

Uses the LLM only for classification, not facts

### 4. MCP Tool Invocation

The agent calls the MCP client, which:

Sends a JSON-RPC request to the MCP server

Includes a unique request ID

Waits for a response with timeout protection

### 5. MCP News Server Processing

The MCP server:

Validates the JSON-RPC request

Queries Google News RSS

Filters articles relevant to the entity

Returns:

result → structured news data

error → if no news is found

### 6. Grounded Summarization

If news is found, Gemini is instructed to:

Use only the provided news

Avoid speculation

Produce a concise, factual summary

### 7. Final Output

The agent prints:

The summarized result

A clear source attribution

If no news exists, the agent explicitly states that no verified public news was found.


# Error Handling & Responsible AI
In this section, I
- The agent will clearly declare that there is no public news.
- There are no assumptions or made-up insights produced.

---

# Setup Instructions

### Prerequisites
- Python 3.10+
- Gemini API key

### Environment Variables
Create a `.env` file in the project root:

GEMINI_API_KEY=your_gemini_api_key_here

#### Obtain a Gemini API Key:

1. Visit: https://ai.google.dev/

2. Create a project

3. Generate an API key

3. Copy the key

### Install Dependencies 
pip install -r requirements.txt 

### Run 
python agent.py 

---

## Notes 
-In this project, high-level frameworks are avoided in order to be as transparent and in control as possible.

## Conclusion

### This project demonstrates how to build a responsible, production-style AI agent that:

Integrates LLM reasoning with real-world data

Uses tools correctly and safely

Produces trustworthy, explainable outputs

It serves as a strong reference implementation for Market Intelligence Agents, MCP-based architectures, and tool-augmented LLM systems.
