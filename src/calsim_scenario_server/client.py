from httpx import Client

from .schemas import Assumption, Scenario


class CalSimScenarioClient:
    def __init__(self, base_url: str):
        self.client = Client(base_url=base_url)

    def get_assumption_names(self) -> list[str]:
        response = self.client.get("/assumptions")
        response.raise_for_status()
        return [a for a in response.json()]

    def get_assumption(self, kind: str) -> list[Assumption]:
        response = self.client.get(f"/assumptions/{kind}")
        response.raise_for_status()
        return [Assumption.model_validate(a) for a in response.json()]

    def get_scenario(self, name: str = None, id: int = None) -> Scenario:
        params = {"name": name, "id": id}
        params = {k: v for k, v in params.items() if v is not None}
        response = self.client.get("/scenario", params=params)
        response.raise_for_status()
        return Scenario.model_validate(response.json())
