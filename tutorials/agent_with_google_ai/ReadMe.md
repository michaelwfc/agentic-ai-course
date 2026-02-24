# Referece
- [building-live-voice-agents-with-googles-adk](https://learn.deeplearning.ai/courses/building-live-voice-agents-with-googles-adk/lesson/dewdno61/introduction)
- [gemini-cli-code-and-create-with-an-open-source-agent](https://learn.deeplearning.ai/courses/gemini-cli-code-and-create-with-an-open-source-agent/lesson/wrg8ewb6/introduction)
- [AI Guide for Cloud Developers](https://www.youtube.com/watch?v=YfiLUpNejpE&list=PLIivdWyY5sqJio2yeg1dlfILOUO2FoFRx&t=109s)
- [Cost of building and deploying AI models in Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/pricing#openai-models)


# Google  AI Products Introduction

## 1. Apps with Gemini 
- [Generative AI beginner's guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/overview?hl=en)


1. [Gemini App](https://gemini.google.com/app)
![image](../../images/google_ai/gemini_app.png)

2. [Gemini for Google Workspace](https://workspace.google.com/ai)
3. [Gemini for Google Cloud](https://cloud.google.com/gemini)
  
4. [Google for Developers](https://ai.google.dev/gemini-api/docs?hl=en)
  for indenpendent developers
5. [Vertex AI](https://cloud.google.com/vertex-ai)



## 2. Vertex AI Introduction


- [生成式 AI](https://docs.cloud.google.com/docs/generative-ai?hl=zh-cn)
- [Vertex AI documentation](https://docs.cloud.google.com/vertex-ai/docs?hl=en)

### 2.1  Key capabilities of Vertex AI
- [Key capabilities of Vertex AI](https://docs.cloud.google.com/vertex-ai/docs/start/introduction-unified-platform?hl=en)

### 2.2  Vertex AI Interface

- [Vertex AI Interface](https://docs.cloud.google.com/vertex-ai/docs/start/introduction-interfaces?hl=en)
- [Development tools overview](https://docs.cloud.google.com/vertex-ai/docs/general/developer-tools-overview?hl=en)


### 2.3 Vertex AI- Generative Develop Tools

#### Google AI Studio
- [Migrate from Google AI Studio to Vertex AI](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/migrate/migrate-google-ai?hl=en)
- [Google AI Studio Playground](https://aistudio.google.com/prompts/new_chat)
![image](../../images/google_ai/google_ai_studio_playground.png)



#### Vertex AI Studio
- [Vertex AI Studio](https://cloud.google.com/generative-ai-studio?hl=en)

##### Vertex AI Studio in Cloud Console
- [Vertex AI Studio in Cloud Console](https://console.cloud.google.com/vertex-ai/studio/multimodal?hl=en&project=vertex-ai-test-488403)
![image](../../images/google_ai/vertex-ai-console.png)
  

####  Vertex AI console
-[Vertex AI Dashboard](https://console.cloud.google.com/vertex-ai/dashboard?hl=en&project=vertex-ai-test-488403)



#### Vertex AI Agent Builder
- [Vertex AI Agent Builder](https://cloud.google.com/products/agent-builder?hl=en)
- [Vertex AI Agent Engine](https://docs.cloud.google.com/agent-builder/agent-engine/overview?hl=en)


#### ADK

#### Gemini CLI

#### Antigravity
Now powered by Antigravity, build full-stack apps with multiplayer support, polished UI, and secure connections to real-world services.




# Google Vertex AI Development Setting
- [Generative AI beginner's guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/overview?hl=en)
- [Vertex AI quickstart](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/start?hl=en)

## Setting up authentication

Before using any AI models, the first step is to configure API credentials. There are several methods to authenticate with Google's Gemini models, including:
1. Google API key  
2. Vertex AI based authentication.

For more information on setting up your own authentication, visit [Google](https://cloud.google.com/free?hl=en). 

The `--api_key` parameter automatically configures your project for Google's Gemini API, setting up the proper authentication environment variables. In this course your API key is configured for you already.

Run the cell below to create the folder structure for your agent!





## 
```bash
pip install -q google-adk==1.22.1
```


## How to setup Google Vertex AI env

- 1. check the free trial on [vertex-ai](https://cloud.google.com/vertex-ai?hl=en)


## 1.2 Setting up your first agent

Before we dive into building agents, let's set up a new folder structure with ADK's built-in project scaffolding using the `adk create` command.

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



