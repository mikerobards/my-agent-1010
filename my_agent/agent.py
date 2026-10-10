from google.adk.agents.llm_agent import Agent
from pathlib import Path
import json

SHELTERS_PATH = Path(__file__).parent / 'shelters.json'


def load_json(path):
    """Read and return the contents of a JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def load_catalog(path=SHELTERS_PATH):
    """Load the list of shelter records from the shelters file."""
    return load_json(path)


def get_shelter_capacity(shelter_name: str) -> dict:
    """
    Get the capacity of a specified shelter.

    Args:
        shelter_name (str): The name of the shelter.

    Returns:
        dict: A dictionary containing the shelter's capacity, or an error
        message if no shelter with that name exists or it is closed.
    """
    for shelter in load_catalog():
        if shelter['name'].lower() == shelter_name.lower():
            if not shelter['open']:
                return {"error": f"Shelter '{shelter['name']}' is currently closed."}
            return {"name": shelter['name'], "capacity": shelter['capacity']}
    return {"error": f"No shelter named '{shelter_name}' was found."}


def get_shelters_by_county(county_name: str) -> dict:
    """
    Get a list of open shelters in a specified county.

    Args:
        county_name (str): The name of the county.

    Returns:
        dict: A dictionary containing the open shelters in the county, or an
        error message if no open shelters are found in that county.
    """
    shelters_in_county = []
    for shelter in load_catalog():
        if shelter['county'].lower() == county_name.lower() and shelter['open']:
            shelters_in_county.append(shelter)
    if not shelters_in_county:
        return {"error": f"No open shelters found in county '{county_name}'."}
    return {"county": county_name, "shelters": shelters_in_county}


root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant answering questions about shelters.',
    instruction=(
        'Provide information about the parsed json data in the shelters.json file. '
        'Only open shelters are reported. '
        'Use get_shelter_capacity when the user asks how many people a specific, '
        'named shelter can hold. '
        'Use get_shelters_by_county when the user asks which shelters are in a '
        'county or wants to find shelters in a particular area. '
        'If a tool returns an error, such as a shelter being closed or not found, '
        'relay it to the user plainly.'
    ),
    tools=[get_shelter_capacity,
           get_shelters_by_county],
)
