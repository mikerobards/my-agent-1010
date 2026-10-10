import json

import pytest

from my_agent import agent
from my_agent.agent import get_shelter_capacity, get_shelters_by_county

CATALOG = [
    {"id": "T001", "name": "Harlow Street Recreation Center",
        "county": "Velmont", "capacity": 220, "open": True},
    {"id": "T002", "name": "Velmont High Gym",
        "county": "Velmont", "capacity": 150, "open": True},
    {"id": "T003", "name": "St. Odran Parish Gym",
        "county": "Velmont", "capacity": 80, "open": False},
    {"id": "T004", "name": "Quillham Civic Arena",
        "county": "Quillham", "capacity": 500, "open": True},
    {"id": "T005", "name": "Fulton Library Annex",
        "county": "Fulton", "capacity": 40, "open": False},
]


@pytest.fixture(autouse=True)
def fake_catalog(monkeypatch):
    """Point the tools at a fixed catalog instead of shelters.json."""
    monkeypatch.setattr(agent, "load_catalog", lambda: CATALOG)


# get_shelter_capacity

def test_capacity_for_open_shelter():
    assert get_shelter_capacity("Harlow Street Recreation Center") == {
        "name": "Harlow Street Recreation Center",
        "capacity": 220,
    }


def test_capacity_name_match_is_case_insensitive():
    result = get_shelter_capacity("quillham CIVIC arena")
    assert result == {"name": "Quillham Civic Arena", "capacity": 500}


def test_capacity_for_closed_shelter_returns_error():
    result = get_shelter_capacity("St. Odran Parish Gym")
    assert result == {
        "error": "Shelter 'St. Odran Parish Gym' is currently closed."}


def test_capacity_for_unknown_shelter_returns_error():
    result = get_shelter_capacity("Nowhere Hall")
    assert result == {"error": "No shelter named 'Nowhere Hall' was found."}


@pytest.mark.parametrize("partial", ["Harlow Street", "harlow", "  Recreation Center "])
def test_capacity_for_partial_name(partial):
    assert get_shelter_capacity(partial) == {
        "name": "Harlow Street Recreation Center",
        "capacity": 220,
    }


def test_capacity_partial_name_matching_closed_shelter_returns_error():
    result = get_shelter_capacity("Odran")
    assert result == {
        "error": "Shelter 'St. Odran Parish Gym' is currently closed."}


def test_capacity_ambiguous_partial_name_lists_matches():
    result = get_shelter_capacity("Gym")
    assert result == {
        "error": "'Gym' matches more than one shelter.",
        "matches": ["Velmont High Gym", "St. Odran Parish Gym"],
    }


def test_capacity_exact_name_wins_over_partial_matches(monkeypatch):
    catalog = CATALOG + [
        {"id": "T006", "name": "Velmont High Gym Annex",
            "county": "Velmont", "capacity": 60, "open": True},
    ]
    monkeypatch.setattr(agent, "load_catalog", lambda: catalog)
    assert get_shelter_capacity("velmont high gym") == {
        "name": "Velmont High Gym", "capacity": 150}


@pytest.mark.parametrize("blank", ["", "   "])
def test_capacity_blank_name_returns_error(blank):
    assert get_shelter_capacity(
        blank) == {"error": "No shelter name was given."}


# get_shelters_by_county

def test_county_returns_only_open_shelters():
    result = get_shelters_by_county("Velmont")
    assert result["county"] == "Velmont"
    assert [s["name"] for s in result["shelters"]] == [
        "Harlow Street Recreation Center",
        "Velmont High Gym",
    ]


@pytest.mark.parametrize("county", [
    "Velmont County",
    "velmont county",
    "  Velmont  ",
    "VELMONT COUNTY ",
])
def test_county_name_is_normalized(county):
    result = get_shelters_by_county(county)
    assert result["county"].lower() == "velmont"
    assert len(result["shelters"]) == 2


def test_county_with_only_closed_shelters_returns_error():
    assert get_shelters_by_county("Fulton") == {
        "error": "No open shelters found in county 'Fulton'."
    }


def test_unknown_county_returns_error():
    assert get_shelters_by_county("Atlantis County") == {
        "error": "No open shelters found in county 'Atlantis'."
    }


def test_county_word_inside_name_is_kept():
    # Only a trailing " County" is stripped.
    assert get_shelters_by_county("Countyville") == {
        "error": "No open shelters found in county 'Countyville'."
    }


# Data loading

def test_tools_read_from_shelters_file(monkeypatch, tmp_path):
    path = tmp_path / "shelters.json"
    path.write_text(json.dumps(CATALOG[:1]))
    monkeypatch.setattr(agent, "load_catalog", lambda: agent.load_json(path))
    assert get_shelter_capacity("Harlow Street Recreation Center")[
        "capacity"] == 220
    assert "error" in get_shelter_capacity("Velmont High Gym")


def test_real_catalog_has_expected_fields():
    for shelter in agent.load_json(agent.SHELTERS_PATH):
        assert {"name", "county", "capacity", "open"} <= shelter.keys()
