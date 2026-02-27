
# Reference

- [Build your first agent](https://learn.deeplearning.ai/courses/building-live-voice-agents-with-googles-adk/lesson/9in9mv/build-your-first-agent)
- [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview?hl=en)
- [Agent Development Kit (ADK) documents](https://google.github.io/adk-docs/)


# L1: Build your first agent

Welcome to **Building AI News Podcast Agent with Google ADK!** In this lesson, you'll build your first AI agent and give it the power to access real-time information from the web. You'll learn the fundamental structure of an agent and explore the ADK Web UI, which is a convenient way to trace your agent's thinking and interact through live voice conversations.

Throughout this course, you'll be building a complete AI News Podcast Agent that can research the latest AI developments and generate professional audio podcasts. This lesson lays the foundation with a simple agent that can fetch recent AI news from the web.

### What you'll learn
In this lesson, you'll build a simple agent that can fetch recent AI news from the web. An agent is a construct that has an LLM and tools:

- You'll learn about the fundamental structure of an agent
- You'll become familiar with an **LLM** as the brain of the agent providing it the generative language capabilities
- You'll explore **tools** that let the agent take actions in the real world

You'll also explore alternative development approaches including YAML configuration and Web Builder options.



## 1.1 Setting up authentication

Before using any AI models, the first step is to configure API credentials. There are several methods to authenticate with Google's Gemini models, including:
1. Google API key  [Not support Now]
2. Vertex AI based authentication.

For more information on setting up your own authentication, visit [Google](https://cloud.google.com/free?hl=en). 

The `--api_key` parameter automatically configures your project for Google's Gemini API, setting up the proper authentication environment variables. In this course your API key is configured for you already.

Run the cell below to create the folder structure for your agent!

```bash

# export http_proxy="http://127.0.0.1:7897"
# export https_proxy="http://127.0.0.1:7897"
# curl -v https://google.com


gcloud auth init
gcloud auth application-default login
# Your browser has been opened to visit:

#     https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=764086051850-6qr4p6gpi6hn506pt8ejuq83di341hur.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A8085%2F&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fcloud-platform+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fsqlservice.login&state=WIG1sjdDdEJZa2j770KzCc4FnOprh2&access_type=offline&code_challenge=uH8vemdoZKjBJ06raOW_HwORcV0ALh6PJN5aP4u6HnA&code_challenge_method=S256


# Credentials saved to file: [C:\Users\michael\AppData\Roaming\gcloud\application_default_credentials.json]

# These credentials will be used by any library that requests Application Default Credentials (ADC).

# Quota project "vertex-ai-test-488403" was added to ADC which can be used by Google client libraries for billing and quota. Note that some services may still bill the project owning the resource.


GOOGLE_CLOUD_PROJECT_ID="vertex-ai-test-488403"

export GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT_ID
export GOOGLE_CLOUD_LOCATION=global
export GOOGLE_GENAI_USE_VERTEXAI=True

echo $GOOGLE_CLOUD_PROJECT

```

## 1.2 Setting up your first agent

```bash
pip install -q google-adk==1.22.1
```

Before we dive into building agents, let's set up a new folder structure with ADK's built-in project scaffolding using the `adk create` command.

[vertex-ai-test API keys](https://console.cloud.google.com/vertex-ai/studio/settings/api-keys?hl=en&project=vertex-ai-test-488403)


```bash
# First we create our expected agent folder 
# You can explore available option: !adk create --help


# GEMINI_API_KEY="AQ.***"
# !adk create --type=code google_app_01 --model gemini-2.5-flash-native-audio-preview-09-2025 --api_key $GEMINI_API_KEY



$ adk create google_app_01
Choose a model for the root agent:
1. gemini-2.5-flash
2. Other models (fill later)
Choose model (1, 2): 1
1. Google AI
2. Vertex AI
Choose a backend (1, 2): 2

You need an existing Google Cloud account and project, check out this link for details:
https://google.github.io/adk-docs/get-started/quickstart/#gemini---google-cloud-vertex-ai

Enter Google Cloud project ID: vertex-ai-test
Enter Google Cloud region [us-central1]: 

Agent created in E:\projects\agentic-ai-course\tutorials\google_app_01:
- .env
- __init__.py
- agent.py

```


When you run `adk create`, it generates three essential files. 
1. The `.env` file securely stores your API credentials and configuration. 
2. The `__init__.py` file marks the directory as a Python package, nabling proper imports. 
3. Most importantly, the `agent.py` file provides a clean foundation where you'll implement your agent.

File structure:
```
app_01/
    __init__.py
    agent.py
    .env
```

ADK create supports two project types. 
- The `--type=code` option generates a Python-based agent in `agent.py`. 
- The `--type=config` option creates a YAML-based agent configuration.

The `--model` parameter specifies the LLM to be used by the agent. We will override this and experiment with different models as we create the agents in this lesson.

## 1.3 Writing your first `agent.py`

Throughout this course, you will be using the `adk create` command to create folders and then write to its agent.py using the cell magic in the notebook. Cell magic uses specific commands to interact with the files in your new agent folder. You will use `%%writefile FILENAME` to do this.

Let's start with the absolute simplest agent possible—one that has no internet access at all. You'll create an Agent with a unique name, specify the LLM model, and give it basic instructions.

As with any agent, you need an LLM to start with. ADK is model agnostic - meaning you can provide it with any model of your choice like Gemini, Claude, Ollama and even use LiteLLM to bring in other models. In this lesson, you'll be using the Gemini 2.0 flash and Gemini 2.0 flash live models.

```python
%%writefile app_01/agent.py

from google.adk.agents import Agent

model="gemini-2.5-flash-native-audio-preview-09-2025", # Essential for live voice interaction
# model = "gemini-2.5-flash-lite"

root_agent = Agent(
    name="ai_news_agent_simple",
    model=model,
    instruction="You are an AI News Assistant.",
)


```

## 1.4 Running your first agent

Now comes the exciting part—actually using what you've built. ADK gives you several ways to run your agent, but for development and learning, you'll use the ADK Web UI.

To start the local server and access the Web UI, follow the below steps:

**Terminal Instructions**
1. To open the terminal, run the python code block below.
2. When the terminal window opens under the python code block (it may take a few seconds), enter this bash command from the command line prompt: 

`pkill -f "adk web" ; sleep 1 ; cd ~/work/L1 && adk web --host 0.0.0.0 --port 8001`

Here's a closer look at the command that starts the agent.
- **pkill -f "adk web" ; sleep 1 ;**: this command will stop any adk apps that might currently be running on your requested port 8001. This is handy for situations where you may be running an app several times as you learn and update.
- **cd ~/work/L1 &&**: Changes to the directory where the root agent is stored, this may be different on your local environment.
- **adk web --host 0.0.0.0 --port 8001**: This simple A simple command that starts your agent on the Web UI and sets the host address and the port we will access the server from. In this case, port **8001**.


```bash


# michael@DESKTOP-2KLOSPO MINGW64 /e/projects/agentic-ai-course/tutorials (main)

$ adk web --host 0.0.0.0 --port 8001

2026-02-26 15:36:19,392 - INFO - service_factory.py:220 - Using in-memory memory service
2026-02-26 15:36:19,393 - INFO - local_storage.py:83 - Using per-agent session storage rooted at E:\projects\agentic-ai-course\tutorials
2026-02-26 15:36:19,393 - INFO - local_storage.py:109 - Using file artifact service at E:\projects\agentic-ai-course\tutorials\.adk\artifacts
C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\cli\fast_api.py:141: UserWarning: [EXPERIMENTAL] InMemoryCredentialService: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  credential_service = InMemoryCredentialService()
C:\Users\michael\.conda\envs\py311\Lib\site-packages\google\adk\auth\credential_service\in_memory_credential_service.py:33: UserWarning: [EXPERIMENTAL] BaseCredentialService: This feature is experimental and may change or be removed in future versions without notice. It may introduce breaking changes at any time.
  super().__init__()
INFO:     Started server process [19156]
INFO:     Waiting for application startup.

+-----------------------------------------------------------------------------+
| ADK Web Server started                                                      |
|                                                                             |
| ADK Web Server started                                                      |
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://0.0.0.0:8001.                         |
| ADK Web Server started                                                      |
|                                                                             |
| ADK Web Server started                                                      |
| ADK Web Server started                                                      |
|                                                                             |
| For local testing, access at http://0.0.0.0:8001.                         |
+-----------------------------------------------------------------------------+

INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     127.0.0.1:52623 - "GET /dev-ui/?app=google_app_01&session=1a0f335d-6ba6-4a2c-81e6-1fd3498f6978&userId=user HTTP/1.1" 304 Not Modified
INFO:     127.0.0.1:52623 - "GET /dev-ui/assets/config/runtime-config.json HTTP/1.1" 200 OK
INFO:     127.0.0.1:52623 - "GET /list-apps?relative_path=./ HTTP/1.1" 200 OK
INFO:     127.0.0.1:52623 - "GET /builder/app/google_app_01?ts=1772091382989 HTTP/1.1" 200 OK
2026-02-26 15:36:23,073 - INFO - local_storage.py:59 - Creating local session service at E:\projects\agentic-ai-course\tutorials\google_app_01\.adk\session.db
INFO:     127.0.0.1:53852 - "GET /apps/google_app_01/users/user/sessions/1a0f335d-6ba6-4a2c-81e6-1fd3498f6978 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53852 - "GET /debug/trace/session/1a0f335d-6ba6-4a2c-81e6-1fd3498f6978 HTTP/1.1" 200 OK
INFO:     127.0.0.1:53852 - "GET /apps/google_app_01/eval_sets HTTP/1.1" 200 OK
INFO:     127.0.0.1:52623 - "GET /apps/google_app_01/eval_results HTTP/1.1" 200 OK
INFO:     127.0.0.1:52623 - "GET /apps/google_app_01/users/user/sessions HTTP/1.1" 200 OK
INFO:     127.0.0.1:49282 - "POST /run_sse HTTP/1.1" 200 OK
2026-02-26 15:36:32,282 - INFO - envs.py:83 - Loaded .env file for google_app_01 at E:\projects\agentic-ai-course\tutorials\google_app_01\.env
2026-02-26 15:36:32,283 - INFO - envs.py:83 - Loaded .env file for google_app_01 at E:\projects\agentic-ai-course\tutorials\google_app_01\.env
2026-02-26 15:36:32,286 - INFO - agent_loader.py:129 - Found root_agent in google_app_01.agent
2026-02-26 15:36:32,297 - INFO - _api_client.py:640 - The project/location from the environment variables will take precedence over the API key from the environment variables.
2026-02-26 15:36:32,740 - INFO - google_llm.py:181 - Sending out request, model: gemini-2.5-flash-lite, backend: GoogleLLMVariant.VERTEX_AI, stream: False
2026-02-26 15:36:32,741 - INFO - models.py:7481 - AFC is enabled with max remote calls: 10.
2026-02-26 15:36:51,295 - INFO - _api_client.py:1329 - Retrying due to aiohttp error: Cannot connect to host aiplatform.googleapis.com:443 ssl:<ssl.SSLContext object at 0x000001DDF3CD3800> [None]
2026-02-26 15:37:02,749 - INFO - google_llm.py:246 - Response received from the model.
INFO:     127.0.0.1:49282 - "GET /debug/trace/session/1a0f335d-6ba6-4a2c-81e6-1fd3498f6978 HTTP/1.1" 200 OK




```

## 1.5 Adding tools to your agent

```python
# %%writefile app_02/agent.py

from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="ai_news_agent_simple",
    model="gemini-2.5-flash-native-audio-preview-09-2025", # Essential for live voice interaction
    instruction="You are an AI News Assistant. Use Google Search to find recent AI news.",
    tools=[google_search]
)
```


## 1.8 Fine-tuning agent instructions

So far your agent has simple instructions, but for reliable behavior, you need more sophisticated instruction engineering. Let's enhance your agent with strict behavioral controls.

Create a new folder using the `adk create` command.


```python

%%writefile app_05/agent.py

from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="ai_news_agent_strict",
    model="gemini-2.5-flash-native-audio-preview-09-2025",
    instruction="""
    **Your Core Identity and Sole Purpose:**
    You are a specialized AI News Assistant. Your sole and exclusive purpose is to find and summarize recent news (from the last few weeks) about Artificial Intelligence.

    **Strict Refusal Mandate:**
    If a user asks about ANY topic that is not recent AI news, you MUST refuse.
    For off-topic requests, respond with the exact phrase: "Sorry, I can't answer anything about this. I am only supposed to answer about the latest AI news."

    **Required Workflow for Valid Requests:**
    1. You MUST use the `google_search` tool to find information.
    2. You MUST base your answer strictly on the search results.
    3. You MUST cite your sources.
    """,
    tools=[google_search]
)
```

### Understanding Advanced Instructions

This enhanced instruction pattern includes:

- **Clear Identity**: Explicitly defines the agent's sole purpose
- **Refusal Mechanism**: Provides exact phrases for rejecting off-topic requests  
- **Workflow Requirements**: Forces the agent to use tools and cite sources
- **Behavioral Boundaries**: Sets expectations for valid vs. invalid requests

This creates a much more reliable and focused agent behavior.

### Testing Instructions

**Refresh the ADK Web UI**, select the appropriate app (app_05) from the dropdown menu and test your enhanced agent with both valid and invalid requests:

**Valid prompts** (should get a response):
- "What's the latest AI news about Google?"
- "Tell me about recent AI chip developments"

**Invalid prompts** (should be refused):
- "What's the weather today?"
- "Help me with my homework"

Watch how the agent now maintains strict boundaries while still being helpful for AI-related queries.


# L3: Tools for your agent
Welcome to Lesson 3 **Tools for your agent**. In this lesson, you'll learn how to add custom function tools and enhance your agent with external data sources. You'll integrate financial data APIs and build more sophisticated agent instructions—essential skills for building reliable AI applications.


### Understanding Function Tools
What makes a good function tool:

- **Clear Documentation**: Comprehensive docstrings that ADK uses for tool descriptions  
- **Type Annotations**: Essential for ADK's automatic tool registration and schema validation  
- **Robust Error Handling**: Graceful failure modes prevent agent crashes  
- **Consistent Return Format**: Predictable output structure agents can reliably process  

## 3.4 Adding your root agent 
Now let's create your agent with sophisticated instructions that use both the Google Search tool and your custom financial tool.

Let's examine the enhanced instructions:

### Key Instruction Patterns
Notice how these instructions implement several best practices:

1. **Structured Workflow**: 5-step process from clarification to detailed discussion  
2. **Tool Citation Requirements**: Agent must cite google_search and get_financial_context usage  
3. **Interactive Design**: Prompts user for input at each stage rather than providing monologues  
4. **Scope Boundaries**: Clear rules about staying focused on AI news for US-listed companies  
5. **Error Handling**: Graceful responses when asked about off-topic subjects  

This creates a much more reliable and user-friendly conversational experience.



## 3.5 Test Your Agent
Let's test your agent using the ADK Web UI. These steps will be repeated for all lessons in this course.

To start the local server and access the Web UI, follow the below steps:

**Terminal Instructions**
1. To open the terminal, run the python code block below.
2. When the terminal window opens under the python code block (it may take a few seconds), enter this bash command from the command line prompt: 
`pkill -f "adk web" ; sleep 1 ; cd ~/work/L3 && adk web --host 0.0.0.0 --port 8003`

Here's a closer look at the command that starts the agent.
- **pkill -f "adk web" ; sleep 1 ;**: this command will stop any adk apps that might currently be running on your requested port 8003. This is handy for situations where you may be running an app several times as you learn and update.
- **cd ~/work/L1 &&**: Changes to the directory where the root agent is stored, this may be different on your local environment.
- **adk web --host 0.0.0.0 --port 8003**: This simple A simple command that starts your agent on the Web UI and sets the host address and the port we will access the server from. In this case, port **8003**.


### Try This Testing Sequence
Once your agent is running, try this conversation flow to see all the features in action:

1. Start with a general request: "Give me AI news for Google"  
2. Respond to clarification: "Give me 3 top AI news items for publicly traded US tech stocks"  
3. Pick a specific story: "Tell me more about the first one"  
4. Test boundaries: "What's the weather today?" (should be refused)  

Watch how the agent uses both tools in coordination and maintains conversation flow.


## 🎯 3.6 Exercise: Expand Your Tool
Now it's your turn to experiment and enhance the agent! Try these modifications:

### Exercise 1: Add Another Custom Tool
Create a new custom tool and add it to your agent. Here are some ideas:

- **Company Info Tool**: Use an API to get company details (headquarters, CEO, employee count)
- **News Sentiment Tool**: Analyze the sentiment of news headlines (positive/negative/neutral)
- **Market Summary Tool**: Get overall market indices (S&P 500, NASDAQ, Dow Jones)
- **AI Trends Tool**: Track mentions of specific AI technologies (LLM, computer vision, robotics)

**Hint**: Follow the same pattern as get_financial_context - include type annotations, comprehensive docstrings, and robust error handling. 

Don't forget to add your new tool to the agent's tools array!

### Exercise 2: Instruction Refinement
Enhance the agent instructions to:

- Request user preference for number of companies to track (1-5 range)
- Add a disclaimer about financial data being for informational purposes only
- Include timestamp information about when the data was fetched

### Exercise 3: Conversation Flow
Test the conversation boundaries:

- Try asking about non-US companies and see how the agent responds
- Test with different types of AI news (research, products, acquisitions)
- See how the agent handles follow-up questions about specific companies

### Exercise 4: Error Handling
Test the tool's error handling:

- Try requesting financial data for invalid ticker symbols
- Test with companies that might not have complete financial data
- See how the agent handles network connectivity issues

**Pro Tip**: Use the `--reload_agents` flag when starting `adk web` so you can iterate quickly!


## 🎯 3.6 Exercise: Expand Your Tool
Now it's your turn to experiment and enhance the agent! Try these modifications:

### Exercise 1: Add Another Custom Tool
Create a new custom tool and add it to your agent. Here are some ideas:

- **Company Info Tool**: Use an API to get company details (headquarters, CEO, employee count)
- **News Sentiment Tool**: Analyze the sentiment of news headlines (positive/negative/neutral)
- **Market Summary Tool**: Get overall market indices (S&P 500, NASDAQ, Dow Jones)
- **AI Trends Tool**: Track mentions of specific AI technologies (LLM, computer vision, robotics)

**Hint**: Follow the same pattern as get_financial_context - include type annotations, comprehensive docstrings, and robust error handling. 

Don't forget to add your new tool to the agent's tools array!

### Exercise 2: Instruction Refinement
Enhance the agent instructions to:

- Request user preference for number of companies to track (1-5 range)
- Add a disclaimer about financial data being for informational purposes only
- Include timestamp information about when the data was fetched

### Exercise 3: Conversation Flow
Test the conversation boundaries:

- Try asking about non-US companies and see how the agent responds
- Test with different types of AI news (research, products, acquisitions)
- See how the agent handles follow-up questions about specific companies

### Exercise 4: Error Handling
Test the tool's error handling:

- Try requesting financial data for invalid ticker symbols
- Test with companies that might not have complete financial data
- See how the agent handles network connectivity issues

**Pro Tip**: Use the `--reload_agents` flag when starting `adk web` so you can iterate quickly!

# L4: Adding a Research Agent

In this lesson, you'll transform your agent from a conversational interface into a research coordinator that works behind the scenes. You'll learn to implement a **coordinator-dispatcher** pattern where the root agent delegates research work to background processes and saves structured reports for later use.

This architectural shift is crucial for building production AI systems that can handle complex workflows without overwhelming users with intermediate processing details.

**Key Learning Objectives:**

- Create coordinator agents that delegate work silently
- Build agents optimized for background processing
- Implement file persistence with structured markdown reports
- Understand when to use structured schemas vs. free-form output

**Note:** This lesson introduces patterns essential for multi-agent systems and production deployment.

## 4.3 The Coordinator-Dispatcher Architecture Pattern
In this lesson, you'll be implementing a sophisticated architectural pattern that separates user interaction from background processing. This pattern is essential for production AI systems.

### The Challenge: Information Overload
In previous lessons, your agent would research news and immediately read all findings to the user. This creates several problems:

- **Cognitive overload**: Users get overwhelmed with raw research data  
- **Poor user experience**: Long delays while listening to unfiltered information  
- **Inefficient workflows**: No separation between data gathering and content creation  

### The Solution: Coordinator-Dispatcher Pattern
The coordinator-dispatcher pattern solves this by implementing a two-phase workflow:

1. **Coordination Phase**: Root agent acknowledges the request and coordinates background work  
2. **Execution Phase**: Agent silently executes research, analysis, and file persistence  

### Implementation Strategy
You'll add a save_news_to_markdown tool that:

- Takes research from google_search and get_financial_context  
- Structures the data into a readable markdown report  
- Saves results as ai_research_report.md  
- Enables the root agent to work as a coordinator, not a presenter  

This architectural shift prepares you for the podcast generation system you'll build in later lessons.

### Financial Context Tool: Reusing Existing Components
You'll start by implementing the same financial data tool from Lesson 2.


## 4.5 Advanced Agent Instructions: Implementing Coordinator Behavior

### Adding a root agent
Now you'll configure your agent with sophisticated instructions that implement the coordinator-dispatcher pattern.

### Key Architectural Changes
Compared to previous agents, you'll be implenting  several critical improvements using instructions that demonstrate several advanced patterns:

- **Explicit role definition**: Provide a clear identity as "background research coordinator"
- **Strict workflow specification**: Step-by-step execution requirements
- **Output schema enforcement**: Exact format requirements for consistency
- **Error Handling**: Graceful failure modes at each step and
- **Behavioral Constraints**


# L5: Instruction Tuning and Guardrails

In this lesson, you'll take everything you've learned from previous lessons and add advanced control mechanisms that transform your agents from helpful assistants into specialized, production-ready systems.

### What's new in Lesson 5

Now you'll add another piece: **programmatic control systems** to ensure your agents behave reliably in production environments:

- **Callback Systems**: Programmatic guardrails that automatically enforce policies
    1. **Domain Filtering**: Before Tool callback that blocks certain sources thus controlling information access
    2. **Response Enhancement**: After Tool callback that adds transparency and audit trails into agent outputs
- **Update agent's instructions**: We'll update the agent's instructions to make it callback-aware.

By the end of this lesson, you'll have a production-ready agent that uses all the tools from previous lessons but with effective control mechanisms.

## 5.3 Callbacks

Now you'll implement the core of this lesson: **callback-based control mechanisms**. Callbacks are Python functions that run at specific checkpoints in an agent's lifecycle, providing programmatic control over behavior.

### Understanding ADK Callback types

ADK provides several callback points:
- **before_agent_callback**: Runs before agent execution starts
- **after_agent_callback**: Runs after agent execution completes  
- **before_tool_callback**: Runs before any tool is executed
- **after_tool_callback**: Runs after any tool completes
- **before_model_callback**: Runs before LLM calls
- **after_model_callback**: Runs after LLM responses

### Callback 1: Source filtering Callback (Before Tool Callback)

This callback demonstrates **programmatic policy enforcement**. It automatically blocks search queries that require the agent to fetch news from certain sources.

#### How It Works:

  1. **Interception**: Runs before every `google_search` tool call
  2. **Query analysis**: Examines the search query for blocked domains
  3. **Policy enforcement**: Blocks searches targeting certain sources like Wikipedia, Reddit, Medium
  4. **Error response**: Returns structured error messages when domains are blocked
  5. **Transparency**: Logs allowed/blocked decisions for debugging


Note how the error messages are descriptive!


### Callback 2: Response enhancement (After Tool Callback)

The next callback demonstrates a sophisticated pattern: **response enhancement**. Instead of blocking requests, this callback enriches tool responses with additional metadata.

In previous lessons, when tools returned results, the agent had no visibility into what control mechanisms were active. This callback solves that by making the control system transparent to the LLM. This pattern is crucial for enterprise deployments where audit trails and transparency are required.

#### How this callback works

When this callback is triggered after the tool execution (google_search), the following actions are taken:

1. **Callback trigger**: Monitors when `google_search` tools finish execution.
2. **Domain extraction**: Automatically parses URLs from search results to identify source domains.
3. **State management**: Maintains a persistent log across multiple tool calls using `tool_context.state`.
4. **Response transformation**: Converts simple string responses into structured data with metadata.
5. **Write to the report**: Makes callback actions visible to the LLM through process logs. This log is written to the generated markdown report.

This pattern transforms your agent from a "black box" into a transparent, auditable system suitable for production deployment.



## 5.4 Modifying the agent

Now, let's update the agent.

1) First, add the before and after tool callbacks to the agent. 

```
    before_tool_callback=[filter_news_sources_callback],
    after_tool_callback=[inject_process_log_after_search],
```

2) Then, **modify the agent's instructions** to add the following:

```    
    **Understanding Callback-Modified Tool Outputs:**
    The `google_search` tool is enhanced by pre- and post-processing callbacks. 
    Its final output is a JSON object with two keys:
    1.  `search_results`: A string containing the actual search results.
    2.  `process_log`: A list of strings describing the filtering actions performed, including which domains were sourced.

    **Callback System Awareness:**
    You have a before tool callback "filter_news_sources_callback" that will automatically intercepts or 
    blocks your tool calls. Ensure you call it before each tool.

    **When Testing Callbacks:**
    If users ask you to test the callback system, be conversational and explain what's happening:
    - Acknowledge when callbacks modify your search queries
    - Describe the policy enforcement you observe
    - Help users understand how the layered control system works in practice
```

The instructions are now callback-aware, meaning the agent understands that tool outputs have been enhanced. The workflow accommodates structured reporting that includes process logs, and the agent meets enterprise-ready requirements for error handling and transparency.

## 5.5 Testing the agent

Let's test your agent that combines everything from previous lessons with the new callback-based control systems.

To start the local server and access the Web UI, follow the below steps:

**Terminal Instructions**
1. To open the terminal, run the python code block below.
2. When the terminal window opens under the python code block (it may take a few seconds), enter this bash command from the command line prompt: 
`pkill -f "adk web" ; sleep 1 ; cd ~/work/L5 && adk web --host 0.0.0.0 --port 8001`

Here's a closer look at the command that starts the agent.
- **pkill -f "adk web" ; sleep 1 ;**: this command will stop any adk apps that might currently be running on your requested port 8003. This is handy for situations where you may be running an app several times as you learn and update.
- **cd ~/work/L1 &&**: Changes to the directory where the root agent is stored, this may be different on your local environment.
- **adk web --host 0.0.0.0 --port 8001**: This simple A simple command that starts your agent on the Web UI and sets the host address and the port we will access the server from. In this case, port **8001**.

### Testing the Callbacks

The callback system will automatically:
- Block searches to certain domains (wikipedia, reddit, etc.)
- Log which professional sources are being used in the markdown file
- Inject process information into the final report
- Maintain transparency about control mechanisms

Open the proxy URL below and try asking: 
- "Find me the latest AI news" and watch how the callbacks work behind the scenes!
- "Can you explain the different callbacks you have?". The agent is callback aware and should be able to walk through how the callbacks work.

**Run the cell below and open the link in a new tab.**