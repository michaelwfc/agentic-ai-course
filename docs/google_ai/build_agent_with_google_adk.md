
# Reference

- [Vertex AI Agent Builder overview](https://docs.cloud.google.com/agent-builder/overview?hl=en)


# 1. Vertex AI Development Setting
- [Build your first agent](https://learn.deeplearning.ai/courses/building-live-voice-agents-with-googles-adk/lesson/9in9mv/build-your-first-agent)

## 1.1 Setting up authentication

Before using any AI models, the first step is to configure API credentials. There are several methods to authenticate with Google's Gemini models, including:
1. Google API key  [Not support Now]
2. Vertex AI based authentication.

For more information on setting up your own authentication, visit [Google](https://cloud.google.com/free?hl=en). 

The `--api_key` parameter automatically configures your project for Google's Gemini API, setting up the proper authentication environment variables. In this course your API key is configured for you already.

Run the cell below to create the folder structure for your agent!


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
export http_proxy="http://127.0.0.1:7897"
export https_proxy="http://127.0.0.1:7897"
curl -v https://google.com

# michael@DESKTOP-2KLOSPO MINGW64 /e/projects/agentic-ai-course/tutorials (main)
$ adk web --host 0.0.0.0 --port 8001

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