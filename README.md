# Clinware-AI-agent

# Overview
The development of this system involves creating a **Market Intelligence AI Agent** that will produce well-founded insights concerning **Clinware**, which is an AI company that provides post-acute care.
The agent adopts **Gemini tool calling** and **local MCP-compliant news server** to acquire the public news and generate summaries without hallucinations.

The system is intended to illustrate:
     The following:
- Tool Calling with LLMs
- Client/server communication using the MCP
- JSON-RPC protocol usage
- AI answers grounded in observations about the
- Elegant Error Handling


## Key Features
- **Dynamic Tool Calling**: It is the job of the LLM to determine if any external data needs to be fetched
- **MCP Integration**: An MCP-style server locally retrieves real-time news via the NewsAPI.
- **JSON-RPC Communication**: This is done through JSON-RPC over standard input/output. 
- **Grounded Responses**: The responses generated are strictly on the basis of data provided by the tool. 
- **Graceful Fallbacks**: In the absence of publicly known news, the agent states this fact instead of hallucinating.

---

##  System Architecture

User Query  
↓  
Gemini LLM (Tool Calling + System Prompt)  

            ↓ decides tool invocation  
search_clinware_news (Tool)  

            ↓  
MCP Client (JSON-RPC over stdio)  

            ↓  
Local MCP News Server  

            ↓  
NewsAPI (Real-time Public News)  

            ↓  
Structured News Data  

            ↓  
Gemini LLM (Grounded Summary)  

            ↓  
Final Market Intelligence Output  


The architecture ensures that all responses are grounded in real-time data fetched via an MCP-compliant server, preventing hallucinations.

---

##How It Works
===============
1. Question related to Clinware by user.
2. Gemini carries out the querying process through the utilization of the system prompt as well as the tool schematics.
3. In the event that real-time data is required, Gemini invokes the MCP utility.
4. The MCP client sends a JSON-RPC request to the local MCP server.
5. The NewsAPI fetches the news on the MCP server, returning the results in structured form.
6. LLM automatically generates the complete summary from the information provided to it.

---

## Error Handling & Responsible AI
In this section, I
- The agent will clearly declare that there is no public news.
- There are no assumptions or made-up insights produced.
- APIs which are broken or which return nothing.

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- NewsAPI Key
- Gemini API key

### Environment Variables
Add a `.env` file:
NEWS_API_KEY=user_newsapi_key
GEMINI_API_KEY=user_gemini_api_key

### Install Dependencies 
pip install -r requirements.txt 

### Run 
python agent.py 

---

## Notes 
-In this project, high-level frameworks are avoided in order to be as transparent and in control as possible. 
- Architecture is compatible with official MCP servers such as the Verge News MCP Server.
