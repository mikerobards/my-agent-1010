from google.adk.agents.llm_agent import Agent
import json


def get_shelter_capacity(shelter_name: str) -> dict:
    """
    Get the capacity of a specified shelter.

    Args:
        shelter_name (str): The name of the shelter.

    Returns:
        dict: A dictionary containing the shelter's capacity.
    """
    with open('my_agent/shelters.json', 'r') as f:
        shelter_data = json.load(f)
    capacity = [shelter['capacity']
                for shelter in shelter_data if shelter['name'] == shelter_name]
    return {"capacity": capacity}


root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction='Provide information about the parsed json data.',
    tools=[get_shelter_capacity],

)
