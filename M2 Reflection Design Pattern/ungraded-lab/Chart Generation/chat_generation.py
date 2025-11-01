import os
import re
import json
from env_utils import get_env, load_env

load_env()

# Local helper module
import utils



def generate_chart_code(instruction: str, model: str, out_path_v1: str) -> str:
      """Generate Python code to make a plot with matplotlib using tag-based wrapping."""

      prompt = f"""
      You are a data visualization expert.

      Return your answer *strictly* in this format:

      <execute_python>
      # valid python code here
      </execute_python>

      Do not add explanations, only the tags and the code.

      The code should create a visualization from a DataFrame 'df' with these columns:
      - date (M/D/YY)
      - time (HH:MM)
      - cash_type (card or cash)
      - card (string)
      - price (number)
      - coffee_name (string)
      - quarter (1-4)
      - month (1-12)
      - year (YYYY)

      User instruction: {instruction}

      Requirements for the code:
      1. Assume the DataFrame is already loaded as 'df'.
      2. Use matplotlib for plotting.
      3. Add clear title, axis labels, and legend if needed.
      4. Save the figure as '{out_path_v1}' with dpi=300.
      5. Do not call plt.show().
      6. Close all plots with plt.close().
      7. Add all necessary import python statements

      Return ONLY the code wrapped in <execute_python> tags.
      """

      response = utils.get_response(model, prompt)
      return response
    

class ChatGeneration:
  
  def run_generate_chart_code_v1(self):
    # Generate initial code
    code_v1 = generate_chart_code(
        instruction="Create a plot comparing Q1 coffee sales in 2024 and 2025 using the data in coffee_sales.csv.", 
        model="gpt-4o-mini", 
        out_path_v1="chart_v1.png"
    )

    utils.print_html(code_v1, title="LLM output with first draft code")
    return code_v1
  
    
  
  def run_agent_workflow(self, task_id: str, prompt: str, initial_plan_steps: list) -> str:
    """Run the agent workflow."""

    # Load the dataset
    self.load_dataset()

    # Generate the chart code
    chart_code = self.generate_chart_code(prompt, 'gpt-4', 'output.png')

    # Execute the chart code

  def load_dataset(self) :
    # Use this utils.py function to load the data into a dataframe
    df = utils.load_and_prepare_data('coffee_sales.csv')

    # Grab a random sample to display
    utils.print_html(df.sample(n=5), title="Random Sample of Coffee Sales Data")
    
if __name__ == "__main__":
    chat_gen = ChatGeneration()
    chat_gen.run_generate_chart_code_v1()
    

  
  