# Review Log

## Velmont exact match risk

The tool originally exact-matched the county name, which could lead to a situation where a user asks for "Velmont County" and the tool returns no results because the county is listed as "Velmont" in the data. The tool now ignores a trailing "County" in the user's input, allowing it to match "Velmont County" with "Velmont" in the data.

## The two weak asserts

'test_tools_read_from_shelters_file' ends with assert "error" in get_shelter_capacity("Velmont High Gym"). Any error passes, so it can’t tell “not found” from “closed” or “ambiguous”.
'test_county_name_is_normalized' checks len(result["shelters"]) == 2. It would pass if the tool returned two wrong shelters.

Both tests now assert exact results. 'test_tools_read_from_shelters_file' expects the specific not-found error, {"error": "No shelter named 'Velmont High Gym' was found."}, since the gym is in the test catalog but not in the one-shelter file it writes; it also checks the full Harlow Street result rather than just the capacity. 'test_county_name_is_normalized' now checks the shelter names, ["Harlow Street Recreation Center", "Velmont High Gym"], so wrong or closed shelters fail the test.

## Partial name matching

The tool now allows partial name matching for shelters. If a user provides a partial name that matches multiple shelters, the tool will list the matches and ask the user to clarify which shelter they mean. This change improves the user experience by providing more flexibility in how users can query shelter information.

## Off-topic questions

The tool is designed to only answer questions about shelter capacity and open shelters by county. If a user asks a general question that is not about these topics, the tool will politely decline to answer it.
