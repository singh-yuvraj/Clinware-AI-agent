# Clinware-AI-Agent

## Overview

The Clinware Market Intelligence Agent is a **production-style AI research assistant** designed to provide **factually grounded market intelligence** about companies, products, and organizations using **verified public news sources only**.

The agent is intentionally built to **separate reasoning from data access**, ensuring that no responses are generated from model assumptions or training data.

---

## The Agent Combines

- **Google Gemini (LLM)** for intent understanding, subject extraction, and contextual summarization  
- **A local MCP-compliant News Server** for real-time data retrieval  
- **JSON-RPC–based client/server communication**  
- **Google News RSS** as a verifiable, public, non-hallucinated data source  

---

## Project Goals

This project demonstrates how to build an AI agent that:

- Knows **when and how** to fetch real-world data  
- Uses **external tools responsibly**  
- Never hallucinates news or facts  
- Separates **LLM reasoning** from **data retrieval**

---

## Key Capabilities

### Intent-Aware Query Handling
- Accepts natural language queries  
- Understands user intent (overview, funding, activities, updates, etc.)  
- Adapts responses **only when supported by news data**

### MCP-Based Tool Invocation
- Uses a **local MCP News Server** as the sole source of factual data  
- Gemini generates **RSS-compatible search keywords**  
- MCP executes the search and returns structured news results  

### JSON-RPC Communication
- Client/server interaction over **standard input/output**  
- Fully compliant with **JSON-RPC 2.0**  
- Includes request IDs, structured responses, and error handling  

### Grounded AI Responses
- News summaries are generated **only from MCP-provided data**  
- No external assumptions or background knowledge  
- Explicitly states when information is not available  

### Graceful Error Handling
Handles:
- No news found  
- MCP server timeouts  
- API rate limits  

All failures result in **clear, non-misleading responses**.

### Professional Research-Agent Behavior
- Avoids speculative answers  
- Avoids biographical guesses unless explicitly present in news  
- Responds conservatively when information is incomplete  

---

## System Architecture

User Query  
↓  
Gemini LLM (Intent Understanding + Subject Extraction)  

  ↓ decides external data is required  
  
MCP News Search Tool  

  ↓ executes via  
  
MCP Client (JSON-RPC over stdio)  

  ↓  
Local MCP News Server  

  ↓  
Google News RSS (XML Feed)  

  ↓  
Structured News Data  

  ↓  
Gemini LLM (Strict, Grounded Summarization)  

  ↓  
Final Market Intelligence Output  


> All responses are grounded in **real-time public news** retrieved via an MCP-compliant server.

---

## How It Works

### 1. User Input

The user enters a natural language query, such as:

What is the latest news on Clinware funding?

### 2. Subject Extraction (LLM Reasoning)

Gemini is used to:
- Identify the **main subject** that news articles would be written about  
- Produce a **clean RSS search term**  

This step:
- Avoids hardcoded company lists  
- Uses the LLM **only for classification**, not facts  

### 3. MCP Tool Invocation

The agent calls the MCP client, which:
- Sends a JSON-RPC request to the MCP server  
- Includes a unique request ID  
- Waits for a response with timeout protection  

### 4. MCP News Server Processing

The MCP server:
- Validates the JSON-RPC request  
- Queries Google News RSS  
- Performs robust keyword-based filtering  
- Returns:
  - `result` → structured news articles  
  - `error` → when no news is found  

### 5. Grounded Summarization

If news is found, Gemini is instructed to:
- Use **only** the provided news data  
- Avoid speculation or inference  
- Tailor the wording to the user’s question  

### 6. Final Output

The agent prints:
- A concise, factual answer  
- Clear source attribution  

If no relevant news exists, the agent explicitly states that **no verified public news was found**.

---

## Error Handling & Responsible AI

- The agent clearly declares when no public news exists  
- No assumptions or fabricated information are produced  
- All factual content originates from Google News RSS  

This ensures **responsible, explainable AI behavior**.

---

## Setup Instructions

### Prerequisites
- Python 3.10+  
- Gemini API Key

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

- Integrates LLM reasoning with real-world data

- Uses external tools safely and deterministically

- Produces trustworthy, explainable outputs
