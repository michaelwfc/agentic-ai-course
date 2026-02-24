# Import libraries needed for the lesson
# pip install 'pydantic[email]
from typing import Annotated, List, Literal, Union
from pydantic import BaseModel, ValidationError, EmailStr, Field,field_validator,AfterValidator
import json



def check_age(value):
    """
    https://docs.pydantic.dev/latest/concepts/validators/#field-validators
    """
    if value < 18:
        raise ValueError(f"Age must be at least 18,input value is {value}")
    return value


# Create a Pydantic model for validating user input
class UserInput(BaseModel):
    name: str
    email: EmailStr
    query: str

    # age: int = Field(None, description="User's age")
    age: Annotated[int,AfterValidator(check_age)] = Field(None, description="User's age")


    # @field_validator("age",mode="after")
    # @classmethod
    # def check_age(cls, value):
    #     """
    #     https://docs.pydantic.dev/latest/concepts/validators/#field-validators
    #     """
    #     if value < 18:
    #         raise ValueError(f"Age must be at least 18,input value is {value}")
    #     return value


# Define a function to handle user input validation safely
def validate_user_input(input_data):
    try:
        # Attempt to create a UserInput model instance from user input data
        user_input = UserInput(**input_data)
        print(f"✅ Valid user input created:")
        print(f"{user_input.model_dump_json(indent=2)}")
        return user_input
    except ValidationError as e:
        # Capture and display validation errors in a readable format
        print(f"❌ Validation error occurred:")
        for error in e.errors():
            print(f"  - {error['loc'][0]}: {error['msg']}")
        return None
    

if __name__ == "__main__":
    # Create a model instance
    example_01 = {
        "name": "Joe User",
        "email": "joe.user@example.com",
        "query": "I forgot my password."
    }
    
    user_input_01 = UserInput(**example_01)
    print(user_input_01)

    user_input = UserInput.model_validate(example_01)
    json_str = user_input_01.model_dump_json(indent=2)
    
    # Validate the user input using the Pydantic model

    example_02 = {
        "name": "Joe User",
        "email": "not-an-email",
        "query": "I forgot my password."
    }
    try:
        user_input_02 = UserInput(**example_02)
        print(user_input_02)
    except ValidationError as e:
        print(e)


    example_03 = {
        "name": "Joe User",
        "email": "joe.user@example.com",
        "query": "I forgot my password.",
        "age": 5
    }
    try:
        user_input_03 = UserInput(**example_03)
    except ValidationError as e:
        print(e)

