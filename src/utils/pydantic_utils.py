from pydantic import BaseModel, ValidationError, Field, EmailStr,field_validator
from typing import List, Literal, Optional
import json
from datetime import date
# import instructor
from utils.env_utils import load_env
from utils.qwen_api import call_qwen_with_openai_client, QWEN_PLUS



# Define a function to validate an LLM response
def validate_with_model(data_model:BaseModel, llm_response:str)->[BaseModel, str]:
    try:
        validated_data = data_model.model_validate_json(llm_response)
        print("data validation successful!")
        print(validated_data.model_dump_json(indent=2))
        return validated_data, None
    except ValidationError as e:
        print(f"error validating data: {e}")
        error_message = (
            f"This response generated a validation error: {e}."
        )
        return None, error_message
    

# Define a function to create a retry prompt with error feedback
def create_retry_prompt(
    original_prompt, original_response, error_message
):
    retry_prompt = f"""
    This is a request to fix an error in the structure of an llm_response.
    Here is the original request:
    <original_prompt>
    {original_prompt}
    </original_prompt>

    Here is the original llm_response:
    <llm_response>
    {original_response}
    </llm_response>

    This response generated an error: 
    <error_message>
    {error_message}
    </error_message>

    Compare the error message and the llm_response and identify what needs to be fixed or removed in the llm_response to resolve this error. 

    Respond ONLY with valid JSON. Do not include any explanations or other text or formatting before or after the JSON string.
    """
    return retry_prompt



# Define a function to automatically retry an LLM call multiple times
def validate_llm_response(
    prompt, data_model:BaseModel, n_retry=5, 
    model=QWEN_PLUS, # "gpt-4o"
):
    # Initial LLM call
    response_content = call_qwen_with_openai_client(prompt)
    current_prompt = prompt

    # Try to validate with the model
    # attempt: 0=initial, 1=first retry, ...
    for attempt in range(n_retry + 1):

        validated_data, validation_error = validate_with_model(
            data_model, response_content
        )

        if validation_error:
            if attempt < n_retry:
                print(f"retry {attempt} of {n_retry} failed, trying again...")
            else:
                print(f"Max retries reached. Last error: {validation_error}")
                return None, (
                    f"Max retries reached. Last error: {validation_error}"
                )

            validation_retry_prompt = create_retry_prompt(
                original_prompt=current_prompt,
                original_response=response_content,
                error_message=validation_error
            )
            response_content = call_qwen_with_openai_client(validation_retry_prompt)
            current_prompt = validation_retry_prompt
            continue

        # If you get here, both parsing and validation succeeded
        return validated_data, None


# Define UserInput model
class UserInput(BaseModel):
    name: str
    email: EmailStr
    query: str
    order_id: Optional[int] = Field(
        None,
        description="5-digit order number (cannot start with 0)",
        ge=10000,
        le=99999
    )
    purchase_date: Optional[date] = None

    # Validate order_id format (e.g., ABC-12345)
    @field_validator("order_id")
    def validate_order_id(cls, order_id):
        import re
        if order_id is None:
            return order_id
        pattern = r"^[A-Z]{3}-\d{5}$"
        if not re.match(pattern, order_id):
            raise ValueError(
                "order_id must be in format ABC-12345 "
                "(3 uppercase letters, dash, 5 digits)"
            )
        return order_id
    


# Define the CustomerQuery model that inherits from UserInput
class CustomerQuery(UserInput):
    priority: str = Field(..., description="Priority level: low, medium, high" )
    category: Literal['refund_request', 'information_request', 'other' ] = Field(..., description="Query category")
    is_complaint: bool = Field(..., description="Whether this is a complaint")
    tags: List[str] = Field(..., description="Relevant keyword tags")


def build_prompt_with_json(user_input:BaseModel,example_response_structure:str ):
    
    # Create prompt with user data and expected JSON structure
    prompt = f"""
    Please analyze this user query\n {user_input.model_dump_json(indent=2)}:

    Return your analysis as a JSON object matching this exact structure 
    and data types:
    {example_response_structure}

    Respond ONLY with valid JSON. Do not include any explanations or 
    other text or formatting before or after the JSON object.
    """
    return prompt

def build_prompt_with_json_schema(user_input:BaseModel, data_model_schema:str):
    # Create new prompt with user input and model_json_schema
    prompt = f"""
    Please analyze this user query\n {user_input.model_dump_json(indent=2)}:

    Return your analysis as a JSON object matching the following schema:
    {data_model_schema}

    Respond ONLY with valid JSON. Do not include any explanations or 
    other text or formatting before or after the JSON object.
    """
    return prompt


def build_prompt(user_input:BaseModel):
    
    # Create prompt with user data and expected JSON structure
    prompt = f"""
    Please analyze this user query\n {user_input.model_dump_json(indent=2)}:

    and provide a structured response
    """
    return prompt


def get_user_input()->UserInput:
    """Validate user input from a JSON string and return a UserInput  instance if valid."""
    # Define a JSON string representing user input
    user_input_json = '''
    {
        "name": "Joe User",
        "email": "joe.user@example.com",
        "query": "I forgot my password.",
        "order_number": null,
        "purchase_date": null
    }
    '''
    try:
        # Create UserInput instance from JSON data
        user_input = (
            UserInput.model_validate_json(user_input_json)
        )
        print("user input validated...")
        return user_input
    except Exception as e:
        print(f" Unexpected error: {e}")
        return None

    

def run_llm_with_json() -> None:
    print("\nRunning LLM with JSON...")
    user_input =  get_user_input()

    # Create a prompt with generic example data to guide LLM.
    example_response_structure = f"""{{
        name="Example User",
        email="user@example.com",
        query="I ordered a new computer monitor and it arrived with the screen cracked. I need to exchange it for a new one.",
        order_id=12345,
        purchase_date="2025-12-31",
        priority="medium",
        category="refund_request",
        is_complaint=True,
        tags=["monitor", "support", "exchange"] 
    }}"""

    prompt = build_prompt_with_json(user_input, example_response_structure)

    # Attempt to parse the response into CustomerQuery model
    try:
      response = call_qwen_with_openai_client(prompt)
      # print(response)
      valid_data = CustomerQuery.model_validate_json(response)
      # print(valid_data)
      return valid_data
    except Exception as e:
      print(f"Error parsing response: {e}")


    # print(parse_and_validate_user_input(user_input))
    # Test your complete solution with the original prompt
    validated_data, error = validate_llm_response(
    prompt, CustomerQuery
    )
    print(validated_data)





def run_llm_with_json_schema():
    print("\nRun LLM with json schema")
    user_input = get_user_input()
    # Investigate the model_json_schema for CustomerQuery
    data_model_schema = json.dumps(
        CustomerQuery.model_json_schema(), indent=2
    )
    # print(data_model_schema)

    prompt = build_prompt_with_json_schema(user_input, data_model_schema)
    # print(prompt)
    
    # Attempt to parse the response into CustomerQuery model
    try:
      response = call_qwen_with_openai_client(prompt)
      print(response)
      valid_data = CustomerQuery.model_validate_json(response)
      # print(valid_data)
      return valid_data
    except Exception as e:
      print(f"Error parsing response: {e}")
    

    validated_data, error = validate_llm_response(
    prompt, CustomerQuery
    )
    print(validated_data)




def run_llm_with_pydantic():
    print(f"runing llm with pydantic")
    user_input = get_user_input()
    prompt =  build_prompt(user_input)
    
    # Attempt to parse the response into CustomerQuery model
    try:
      response = call_qwen_with_openai_client(prompt,response_format=CustomerQuery)
      print(response)
      valid_data = CustomerQuery.model_validate_json(response)
      print(type(valid_data))
      print(valid_data.model_dump_json(indent=2))
      # print(valid_data)
      return valid_data
    except Exception as e:
      print(f"Error parsing response: {e}")



if __name__ == "__main__":
    load_env()

    
    # run_llm_with_json()
    # run_llm_with_json_schema()
    run_llm_with_pydantic()
    

