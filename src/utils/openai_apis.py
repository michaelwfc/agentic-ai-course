from  openai import OpenAI
from pydantic import BaseModel
# from utils.retry import CustomerQuery

def call_openai_client_create(client:OpenAI, prompt:str, model="gpt-4o"):
    # client = OpenAI()
    response = client.chat.completions.create(
        # model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    response_content =  response.choices[0].message.content
    return response_content


def call_openai_client_parse(client:OpenAI, prompt:str,response_format:BaseModel,  model="gpt-4o"):
    # Initialize OpenAI client and call passing CustomerQuery in your API call
    # openai_client = OpenAI()
    response = client.chat.completions.parse(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        # Use OpenAI's structured output API with your Pydantic schema
        response_format=response_format
    )
    response_content = response.choices[0].message.content
    print(type(response_content))
    print(response_content)
    # response.choices[0].message.parsed
    return response.choices[0].message.content

def call_openai_client_response_api(client:OpenAI, prompt:str, text_format:BaseModel,
                                    model="gpt-4o")->BaseModel:
    # Try the responses API from OpenAI
    response = client.responses.parse(
        model=model,
        input=[{"role": "user", "content": prompt}],
        text_format=text_format
    )

    print(type(response))
    response_output_parsed = response.output_parsed
    return response_output_parsed


# Investigate class inheritance structure of the OpenAI response
def print_class_inheritence(llm_response):
    for cls in type(llm_response).mro():
        print(f"{cls.__module__}.{cls.__name__}")

#print_class_inheritence(response)

def call_openai_client(client:OpenAI, prompt:str,response_format:BaseModel,  
                       model_name="gpt-4o", temperature=0,  use_response_api=False):
    if response_format is None:
        response_content = call_openai_client_create(client, prompt,model=model_name,temperature=temperature)
        return response_content
    elif response_format is not None and issubclass(response_format, BaseModel) and not use_response_api: 
        response_content =  call_openai_client_parse(client, prompt,response_format=response_format, model=model_name)
        return  response_content
    else:
        response_output_parsed = call_openai_client_response_api(client, prompt, text_format=response_format,model=model_name,)
        return response_output_parsed
    
    


