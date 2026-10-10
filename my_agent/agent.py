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
        shelter_name (str): The full or partial name of the shelter. An exact
            name match is preferred; otherwise any shelter whose name contains
            this text matches.

    Returns:
        dict: A dictionary containing the shelter's capacity, or an error
        message if no shelter matches, the shelter is closed, or the partial
        name matches more than one shelter (with the matching names listed).
    """
    query = shelter_name.strip().lower()
    if not query:
        return {"error": "No shelter name was given."}
    catalog = load_catalog()
    matches = [s for s in catalog if s['name'].lower() == query]
    if not matches:
        matches = [s for s in catalog if query in s['name'].lower()]
    if not matches:
        return {"error": f"No shelter named '{shelter_name}' was found."}
    if len(matches) > 1:
        return {
            "error": f"'{shelter_name}' matches more than one shelter.",
            "matches": [s['name'] for s in matches],
        }
    shelter = matches[0]
    if not shelter['open']:
        return {"error": f"Shelter '{shelter['name']}' is currently closed."}
    return {"name": shelter['name'], "capacity": shelter['capacity']}


def get_shelters_by_county(county_name: str) -> dict:
    """
    Get a list of open shelters in a specified county.

    Args:
        county_name (str): The name of the county. A trailing "County"
            (e.g. "Velmont County") is ignored.

    Returns:
        dict: A dictionary containing the open shelters in the county, or an
        error message if no open shelters are found in that county.
    """
    county_name = county_name.strip()
    if county_name.lower().endswith(' county'):
        county_name = county_name[:-len(' county')].rstrip()
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
        'named shelter can hold; a partial name is fine. If it reports that '
        'the name matches more than one shelter, list the matches and ask the '
        'user which one they mean. '
        'Use get_shelters_by_county when the user asks which shelters are in a '
        'county or wants to find shelters in a particular area. '
        'If a tool returns an error, such as a shelter being closed or not found, '
        'relay it to the user plainly. '
        'If the user asks a general question that is not about shelter '
        'capacity or which shelters are open in a county, do not answer it. '
        'Instead, tell the user that this is a shelter information tool and '
        'that you can only help with shelter capacity and open shelters by county.'
    ),
    tools=[get_shelter_capacity,
           get_shelters_by_county],
)
