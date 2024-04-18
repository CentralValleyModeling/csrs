from calsim_scenario_server import clients, schemas

TESTING_DATA = {
    "assumptions": [
        {
            "name": "testing-client-assumption-land-use",
            "kind": "land_use",
            "detail": "test assumption, land use",
        },
        {
            "name": "testing-client-assumption-sea-level-rise",
            "kind": "sea_level_rise",
            "detail": "test assumption, sea level rise",
        },
        # Two hydrology assumptions
        {
            "name": "testing-client-assumption-hydrology-1",
            "kind": "hydrology",
            "detail": "test assumption, hydrology 1",
        },
        {
            "name": "testing-client-assumption-hydrology-2",
            "kind": "hydrology",
            "detail": "test assumption, hydrology 2",
        },
        {
            "name": "testing-client-assumption-tucp",
            "kind": "tucp",
            "detail": "test assumption, tucp",
        },
        {
            "name": "testing-client-assumption-dcp",
            "kind": "dcp",
            "detail": "test assumption, dcp",
        },
        {
            "name": "testing-client-assumption-va",
            "kind": "va",
            "detail": "test assumption, va",
        },
        {
            "name": "testing-client-assumption-south-of-delta",
            "kind": "south_of_delta",
            "detail": "test assumption, south of delta",
        },
    ],
    "scearios": [
        {
            "name": "testing-client-scenario-1",
            "version": None,
            "land_use": "testing-client-assumption-land-use",
            "sea_level_rise": "testing-client-assumption-sea-level-rise",
            "hydrology": "testing-client-assumption-hydrology-1",
            "tucp": "testing-client-assumption-tucp",
            "dcp": "testing-client-assumption-dcp",
            "va": "testing-client-assumption-va",
            "south_of_delta": "testing-client-assumption-south-of-delta",
        },
        {
            "name": "testing-client-scenario-2",
            "version": None,
            "land_use": "testing-client-assumption-land-use",
            "sea_level_rise": "testing-client-assumption-sea-level-rise",
            "hydrology": "testing-client-assumption-hydrology-2",
            "tucp": "testing-client-assumption-tucp",
            "dcp": "testing-client-assumption-dcp",
            "va": "testing-client-assumption-va",
            "south_of_delta": "testing-client-assumption-south-of-delta",
        },
    ],
    "runs": [
        {
            "scenario": "testing-client-scenario-1",
            "version": "0.1",
            "contact": "testing@email.com",
            "code_version": "9.0.0",
            "detail": "Dummy run to test the API client. Scenario 1, is version 0.1",
        },
        {
            "scenario": "testing-client-scenario-1",
            "version": "0.2",
            "parent": "0.1",
            "contact": "update@email.com",
            "code_version": "9.0.1",
            "detail": """Dummy run to test the API client. Scenario 1, is version 0.2,
                        updates were made to the model code.""",
        },
        {
            "scenario": "testing-client-scenario-2",
            "version": "0.1",
            "contact": "other@email.com",
            "code_version": "10.0.0",
            "confidential": False,
            "published": True,
            "detail": "Dummy run to test the API client. Scenario 2, is version 0.1",
        },
    ],
}


def test_local_assumptions(client_local: clients.LocalClient):
    for assumption in TESTING_DATA["assumptions"]:
        s = client_local.put_assumption(**assumption)
        assert isinstance(s, schemas.Assumption)
