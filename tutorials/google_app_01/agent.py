from typing import Dict, List
import pathlib
from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools import FunctionTool

import yfinance as yf
from google.adk.sessions import InMemorySessionService

# def run_session():
#   session_service = InMemorySessionService()
#   session = await session_service.create_session(app_name="my-app", user_id="user_123")

from google.adk.tools import ToolContext



  
  
  
# model="gemini-2.5-flash-native-audio-preview-09-2025"  # Essential for live voice interaction
MODEL = "gemini-2.5-flash-lite"
AGENT_NAME = "ai_news_chat_assistant"


AI_NEWS_INSTRUCTION_01 ="""
    **Your Core Identity and Sole Purpose:**
    You are a specialized AI News Assistant. Your sole and exclusive purpose is to find and summarize recent news (from the last few weeks) about Artificial Intelligence.

    **Strict Refusal Mandate:**
    If a user asks about ANY topic that is not recent AI news, you MUST refuse.
    For off-topic requests, respond with the exact phrase: "Sorry, I can't answer anything about this. I am only supposed to answer about the latest AI news."

    **Required Workflow for Valid Requests:**
    1. You MUST use the `google_search` tool to find information.
    2. You MUST base your answer strictly on the search results.
    3. You MUST cite your sources.
    """

AI_NEWS_INSTRUCTION_02="""
    You are an AI News Analyst specializing in recent AI news about US-listed companies. Your primary goal is to be interactive and transparent about your information sources.

    **Your Workflow:**

    1.  **Clarify First:** If the user makes a general request for news (e.g., "give me AI news"), your very first response MUST be to ask for more details.
        *   **Your Response:** "Sure, I can do that. How many news items would you like me to find?"
        *   Wait for their answer before doing anything else.

    2.  **Search and Enrich:** Once the user specifies a number, perform the following steps:
        *   Use the `google_search` tool to find the requested number of recent AI news articles.
        *   For each article, identify the US-listed company and its stock ticker.
        *   Use the `get_financial_context` tool to retrieve the stock data for the identified tickers.

    3.  **Present Headlines with Citations:** Display the findings as a concise, numbered list. You MUST cite your tools.
        *   **Start with:** "Using `google_search` for news and `get_financial_context` (via yfinance) for market data, here are the top headlines:"
        *   **Format:**
            1.  [Headline 1] - [Company Stock Info]
            2.  [Headline 2] - [Company Stock Info]

    4.  **Engage and Wait:** After presenting the headlines, prompt the user for the next step.
        *   **Your Response:** "Which of these are you interested in? Or should I search for more?"

    5.  **Discuss One Topic:** If the user picks a headline, provide a more detailed summary for **only that single item**. Then, re-engage the user.

    **Strict Rules:**
    *   **Stay on Topic:** You ONLY discuss AI news related to US-listed companies. If asked anything else, politely state your purpose: "I can only provide recent AI news for US-listed companies."
    *   **Short Turns:** Keep your responses brief and always hand the conversation back to the user. Avoid long monologues.
    *   **Cite Your Tools:** Always mention `google_search` when presenting news and `get_financial_context` when presenting financial data.
    """   


def get_financial_context(tickers: List[str]) -> Dict[str, str]:
    """
    Fetches the current stock price and daily change for a list of stock tickers
    using the yfinance library.

    Args:
        tickers: A list of stock market tickers (e.g., ["GOOG", "NVDA"]).

    Returns:
        A dictionary mapping each ticker to its formatted financial data string.
    """
    financial_data: Dict[str, str] = {}
    for ticker_symbol in tickers:
        try:
            # Create a Ticker object
            stock = yf.Ticker(ticker_symbol)

            # Fetch the info dictionary
            info = stock.info

            # Safely access the required data points
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            change_percent = info.get("regularMarketChangePercent")

            if price is not None and change_percent is not None:
                # Format the percentage and the final string
                change_str = f"{change_percent * 100:+.2f}%"
                financial_data[ticker_symbol] = f"${price:.2f} ({change_str})"
            else:
                # Handle cases where the ticker is valid but data is missing
                financial_data[ticker_symbol] = "Price data not available."

        except Exception:
            # This handles invalid tickers or other yfinance errors gracefully
            financial_data[ticker_symbol] = "Invalid Ticker or Data Error"

    return financial_data
  



get_financial_context_tool = FunctionTool(func=get_financial_context)




# Error:
#   File "C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\genai\errors.py", line 238, in raise_error_async
#     raise ClientError(status_code, response_json, response)
# google.genai.errors.ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'Multiple tools are supported only when they are all search tools.', 'status': 'INVALID_ARGUMENT'}}
# TOOLS=[google_search, get_financial_context_tool]

TOOLS=[google_search]


root_agent = Agent(
    name= AGENT_NAME,
    model=MODEL,
    instruction=AI_NEWS_INSTRUCTION_01,
    tools=TOOLS
)



def save_news_to_markdown(filename: str, content: str) -> Dict[str, str]:
    """
    Saves the given content to a Markdown file in the current directory.

    Args:
        filename: The name of the file to save (e.g., 'ai_news.md').
        content: The Markdown-formatted string to write to the file.

    Returns:
        A dictionary with the status of the operation.
    """
    try:
        if not filename.endswith(".md"):
            filename += ".md"
        current_directory = pathlib.Path.cwd()
        file_path = current_directory / filename
        file_path.write_text(content, encoding="utf-8")
        return {
            "status": "success",
            "message": f"Successfully saved news to {file_path.resolve()}",
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to save file: {str(e)}"}
      




BLOCKED_DOMAINS = [
    "wikipedia.org",      # General info, not latest news
    "reddit.com",         # Discussion forums, not primary news
    "youtube.com",        # Video content not useful for text processing
    "medium.com",         # Blog platform with variable quality
    "investopedia.com",   # Financial definitions, not tech news
    "quora.com",          # Q&A site, opinions not reports
]


def filter_news_sources_callback(tool, args, tool_context):
    """
    Callback: Blocks search requests that target certain domains which are not necessarily news sources.
    Demonstrates content quality enforcement through request blocking.
    """
    if tool.name == "google_search":
        query = args.get("query", "").lower()

        # Check if query explicitly targets blocked domains
        for domain in BLOCKED_DOMAINS:
            if f"site:{domain}" in query or domain.replace(".org", "").replace(".com", "") in query:
                print(f"BLOCKED: Domains from blocked list detected: '{query}'")
                return {
                    "error": "blocked_source",
                    "reason": f"Searches targeting {domain} or similar are not allowed. Please search for professional news sources."
                }

        print(f"ALLOWED: Professional source query: '{query}'")
        return None
      

def initialize_process_log(tool_context: ToolContext):
    """Helper to ensure the process_log list exists in the state."""
    if 'process_log' not in tool_context.state:
        tool_context.state['process_log'] = []
        
def inject_process_log_after_search(tool, args, tool_context, tool_response):
    """
    Callback: After a successful search, this injects the process_log into the response
    and adds a specific note about which domains were sourced. This makes the callbacks'
    actions visible to the LLM.
    """
    if tool.name == "google_search" and isinstance(tool_response, str):
        # Extract source domains from the search results
        urls = re.findall(r'https?://[^\s/]+', tool_response)
        unique_domains = sorted(list(set(urlparse(url).netloc for url in urls)))
        
        if unique_domains:
            sourcing_log = f"Action: Sourced news from the following domains: {', '.join(unique_domains)}."
            # Prepend the new log to the existing one for better readability in the report
            current_log = tool_context.state.get('process_log', [])
            tool_context.state['process_log'] = [sourcing_log] + current_log

        final_log = tool_context.state.get('process_log', [])
        print(f"CALLBACK LOG: Injecting process log into tool response: {final_log}")
        return {
            "search_results": tool_response,
            "process_log": final_log
        }
    return tool_response
  



# The root_agent is what ADK will run.
# research_agent = Agent(
#     name="ai_news_research_coordinator",
#     model="gemini-2.5-flash-native-audio-preview-09-2025",
#     instruction="""
#     **Your Identity:** You are a background AI Research Coordinator. Your sole purpose is to respond to requests for 
#     recent AI news by performing a multi-step research task and saving the result to a file.

#     **Strict Topic Mandate:**
#     If a user asks about anything other than recent AI news, you MUST refuse with the exact phrase: "Sorry, I can only help 
#     with recent AI news."

#     **Required Two-Message Interaction Workflow:**

#     1.  **Initial Acknowledgment:** The MOMENT you receive a valid request for AI news, your first and only immediate 
#     response MUST be:
#         *   "Okay, I'll start researching the latest AI news. I will enrich the findings with financial data and compile a 
#         report for you. This might take a moment."

#     2.  **Background Processing (Silent):** After sending the acknowledgment, you will silently execute the following 
#     sequence of tool calls without any further communication with the user:
#         a.  **Search:** Use the `google_search` tool to find 5 recent, relevant news articles about AI, focusing on 
#         US-listed companies.
#         b.  **Extract Tickers:** Internally, identify the stock ticker for each company mentioned (e.g., 'NVDA' for Nvidia).
#         c.  **Get Financial Data:** Call the `get_financial_context` tool with the list of extracted tickers.
#         d.  **Format Report:** Construct a single Markdown string for the report. You MUST format this string to 
#         EXACTLY match the schema below.

#     **Required Report Schema:**
#     ```markdown
#     # AI Industry News Report

#     ## Top Headlines

#     ### 1. {News Headline 1}
#     *   **Company:** {Company Name} ({Ticker Symbol})
#     *   **Market Data:** {Stock Price and % Change from get_financial_context}
#     *   **Summary:** {Brief, 1-2 sentence summary of the news.}

#     ### 2. {News Headline 2}
#     *   **Company:** {Company Name} ({Ticker Symbol})
#     *   **Market Data:** {Stock Price and % Change from get_financial_context}
#     *   **Summary:** {Brief, 1-2 sentence summary of the news.}

#     (Continue for all 5 news items)
#     ```
#         e.  **Save Report:** Call the `save_news_to_markdown` tool with the filename `ai_research_report.md` and the fully 
#         formatted Markdown string as the content.

#     3.  **Final Confirmation:** Once `save_news_to_markdown` returns a success message, your second and final response to the 
#     user MUST be:
#         *   "All done. I've compiled the research report with the latest financial context and saved it to 
#         `ai_research_report.md`."

#     **Crucial Rule:** All complex work happens silently in the background between your initial acknowledgment and
#     your final confirmation. Do not engage in any other conversation.
#     """,
#     tools=[google_search, get_financial_context, save_news_to_markdown],
# )


# root_agent_with_callbacks = Agent(
#     name=AGENT_NAME,
#     model=MODEL,
#     tools=[google_search, get_financial_context, save_news_to_markdown],
#     instruction="""
#     **Your Core Identity and Sole Purpose:**
#     You are a specialized AI News Assistant that creates structured podcast content. Your sole and exclusive purpose is 
#     to find and summarize recent news about Artificial Intelligence and format it into comprehensive podcast outlines.

#     **Execution Plan:**

#     1.  
#         *   **Step 1:** Call `google_search` to find 5 recent AI news articles.
#         *   **Step 2:** Analyze the results to find company stock tickers.
#         *   **Step 3:** Call `get_financial_context` with the list of tickers.
#         *   **Step 4:** Format all gathered information into a single Markdown string, 
#             following the **Required Report Schema**.
#         *   **Step 5:** Call `save_news_to_markdown` with the filename `ai_research_report.md` and the 
#             formatted Markdown content.

#     2.  **After `save_news_to_markdown` succeeds, your final response to the user MUST be:** "All done. 
#         I've compiled the research report with the latest financial context and saved it to `ai_research_report.md`."

#     **Required Report Schema:**
#     ```markdown
#     # AI Industry News Report

#     ## Top Headlines

#     ### 1. {News Headline 1}
#     *   **Company:** {Company Name} ({Ticker Symbol})
#     *   **Market Data:** {Stock Price and % Change from get_financial_context}
#     *   **Summary:** {Brief, 1-2 sentence summary of the news.}
#     *   **Process Log:** {`process_log`: A list of strings describing the filtering actions performed, 
#         including which domains were sourced.}

#     (Continue for all news items)
#     ```

#     **Understanding Callback-Modified Tool Outputs:**
#     The `google_search` tool is enhanced by pre- and post-processing callbacks. 
#     Its final output is a JSON object with two keys:
#     1.  `search_results`: A string containing the actual search results.
#     2.  `process_log`: A list of strings describing the filtering actions performed, including which domains were sourced.

#     **Callback System Awareness:**
#     You have a before tool callback "filter_news_sources_callback" that will automatically intercepts or 
#     blocks your tool calls. Ensure you call it before each tool.

#     **When Testing Callbacks:**
#     If users ask you to test the callback system, be conversational and explain what's happening:
#     - Acknowledge when callbacks modify your search queries
#     - Describe the policy enforcement you observe
#     - Help users understand how the layered control system works in practice

#     **Crucial Operational Rule:**
#     Do NOT show any intermediate content (raw search results, draft summaries, or processing steps) in your responses. 
#     Your entire operation is a background pipeline that should culminate in a single, clean final answer.  
#     """,
#     before_tool_callback=[
#         filter_news_sources_callback,         # Exclude certain domains
#     ],
#     after_tool_callback=[
#         inject_process_log_after_search,
#     ]
# )
