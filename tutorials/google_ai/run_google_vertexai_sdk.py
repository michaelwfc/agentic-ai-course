import vertexai
from vertexai.preview.prompts import Prompt

PROJECT_ID="vertex-ai-test-488403"
LOCATION= "global" #"us-central1"

MODEL_NAME = "gemini-2.5-flash"
# Initialize vertexai
vertexai.init(project=PROJECT_ID, location=LOCATION)

variables = [
    {"animal": "Eagles", "activity": "eat berries"},
    {"animal": "Coyotes", "activity": "jump"},
    {"animal": "Squirrels", "activity": "fly"}
]

# define prompt template
prompt = Prompt(
    prompt_data="Do {animal} {activity}?",
    model_name=MODEL_NAME,
    variables=variables,
    system_instruction="You are a helpful zoologist"
    # generation_config=generation_config, # Optional
    # safety_settings=safety_settings, # Optional
)

# Generates content using the assembled prompt.
responses = []
for variable_set in prompt.variables:
    response = prompt.generate_content(
        contents=prompt.assemble_contents(**variable_set)
    )
    responses.append(response)

for response in responses:
    print(response.text, end="")

# Example response
    # Assembled prompt replacing: 1 instances of variable animal, 1 instances of variable activity
    # Eagles are primarily carnivorous.  While they might *accidentally* ingest a berry......