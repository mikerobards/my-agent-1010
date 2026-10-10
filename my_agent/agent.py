from google.adk.agents.llm_agent import Agent
from pathlib import Path
import json

SHELTERS_PATH = Path(__file__).parent / 'shelters.json'


def load_json(path):
    """Read and return the contents of a JSON file."""
    with open(path, 'r') as f:
        return json.load(f)


def build_catalog(json_data):
    """Index a list of shelter records by shelter id."""
    shelter_catalog = {}
    for shelter in json_data:
        shelter_id = shelter['id']
        shelter_catalog[shelter_id] = {
            'name': shelter['name'],
            'county': shelter['county'],
            'capacity': shelter['capacity'],
            'open': shelter['open'],
        }
    return shelter_catalog


def load_catalog(path=SHELTERS_PATH):
    """Load the shelters file and build the catalog from it."""
    return build_catalog(load_json(path))


def get_shelter_capacity(shelter_name: str) -> dict:
    """
    Get the capacity of a specified shelter.

    Args:
        shelter_name (str): The name of the shelter.

    Returns:
        dict: A dictionary containing the shelter's capacity, or an error
        message if no shelter with that name exists or it is closed.
    """
    for shelter in load_catalog().values():
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
    for shelter in load_catalog().values():
        if shelter['county'].lower() == county_name.lower() and shelter['open']:
            shelters_in_county.append(shelter)
    if not shelters_in_county:
        return {"error": f"No open shelters found in county '{county_name}'."}
    return {"county": county_name, "shelters": shelters_in_county}


root_agent = Agent(
    model='gemini-3.8-flash',
    name='root_agent',
    description='A helpful assistant answering questions about shelters.',
    instruction='Provide information about the parsed json data in the shelters.json file. ',
    tools=[get_shelter_capacity,
           get_shelters_by_county],
)
