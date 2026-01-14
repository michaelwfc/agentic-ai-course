import os
from openai import OpenAI
from env_utils import load_env
from qwen_api import qwen_client, QWEN_PLUS

# === Env & Clients ===
load_env()

# Both clients read keys from env by default; explicit is also fine:


def get_response(prompt: str,model: str=QWEN_PLUS) -> str:
    if "claude" in model.lower() or "anthropic" in model.lower():
        # anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        # anthropic_client = Anthropic(api_key=anthropic_api_key) if anthropic_api_key else Anthropic()
        # Anthropic Claude format
        message = anthropic_client.messages.create(
            model=model,
            max_tokens=1000,
            messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
        )
        return message.content[0].text

    elif "openai" in model.lower() or "gpt" in model.lower():
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else OpenAI()
        # Default to OpenAI format for all other models (gpt-4, o3-mini, o1, etc.)
        response = openai_client.responses.create(
            model=model,
            input=prompt,
        )
        return response.output_text
    else:
        completion = qwen_client.chat.completions.create(
            model= model, #"qwen3-max",  # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        return completion.choices[0].message.content

if __name__ == "__main__":
    print(get_response("Whao are you?"))