# Shelter Agent

A [Google ADK](https://google.github.io/adk-docs/) agent that answers questions about emergency shelters using the data in `my_agent/shelters.json`. It reports only shelters that are open.

## Tools

| Tool | What it does |
| --- | --- |
| `get_shelter_capacity(shelter_name)` | Returns how many people a named shelter can hold. Returns an error if the shelter is closed or doesn't exist. |
| `get_shelters_by_county(county_name)` | Lists the open shelters in a county. Returns an error if the county has none. |

Name matching is case-insensitive.

## Setup

Requires Python 3.10 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `my_agent/.env` with your Gemini API key:

```
GOOGLE_GENAI_USE_ENTERPRISE=FALSE
GOOGLE_API_KEY=your-api-key
```

`.env` is gitignored, so don't commit your key.

## Running

From the project root:

```bash
adk web       # browser chat UI at http://localhost:8000
adk run my_agent  # chat in the terminal
```

Example questions:

- "How many people can Harlow Street Recreation Center hold?"
- "Which shelters are open in Velmont County?"

## Data

`my_agent/shelters.json` is a list of shelter records:

```json
{
  "id": "S001",
  "name": "Harlow Street Recreation Center",
  "county": "Velmont",
  "capacity": 220,
  "open": true
}
```

The tools re-read the file on every call, so edits take effect without restarting the agent.
