# Shelter Agent

A [Google ADK](https://google.github.io/adk-docs/) agent that answers questions about emergency shelters using the data in `my_agent/shelters.json`. It reports only shelters that are open.

## Tools

| Tool | What it does |
| --- | --- |
| `get_shelter_capacity(shelter_name)` | Returns how many people a named shelter can hold. Accepts a partial name ("Harlow" finds Harlow Street Recreation Center); an exact name match wins. Returns an error if the shelter is closed, doesn't exist, or the partial name matches more than one shelter (the error lists the matches). |
| `get_shelters_by_county(county_name)` | Lists the open shelters in a county. A trailing "County" is ignored, so "Velmont" and "Velmont County" both work. Returns an error if the county has none. |

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

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

The tests in `tests/` call both tools directly against a fixed in-test catalog, so they don't need an API key and don't depend on what's in `shelters.json`.

## Evidence

The [`evidence/`](evidence/) folder holds sample runs of the agent:

| File | Shows |
| --- | --- |
| [`adk_run.txt`](evidence/adk_run.txt) | Terminal transcript from `adk run my_agent` covering all the cases below. |
| [Screenshot 14.54.29](evidence/Screenshot%202026-10-10%20at%2014.54.29.png) | `adk web`: capacity lookup for an open shelter (Quillham Civic Arena) and a closed one (St. Odran Parish Gym). |
| [Screenshot 14.55.20](evidence/Screenshot%202026-10-10%20at%2014.55.20.png) | `adk web`: county lookup with open shelters (Velmont) and with none (Fulton). |
| [Screenshot 14.55.58](evidence/Screenshot%202026-10-10%20at%2014.55.58.png) | `adk web`: a general question ("What should I pack for an emergency shelter?") answered without calling a tool. |

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
