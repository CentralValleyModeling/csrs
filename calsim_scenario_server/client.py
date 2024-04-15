from httpx import Client

from .schemas import Assumption, Scenario


class CalSimScenarioClient:
    def __init__(self, base_url: str):
        self.actor = Client(base_url=base_url)

    def get_assumption_names(self) -> list[str]:
        response = self.actor.get("/assumptions")
        response.raise_for_status()
        return [a for a in response.json()]

    def put_assumption(self, name: str, kind: str, detail: str) -> Assumption:
        json = dict(name=name, kind=kind, detail=detail)
        response = self.actor.put(f"/assumptions/{kind}", json=json)
        response.raise_for_status()
        return Assumption.model_validate(response.json())

    def get_assumption(self, kind: str) -> list[Assumption]:
        response = self.actor.get(f"/assumptions/{kind}")
        response.raise_for_status()
        return [Assumption.model_validate(a) for a in response.json()]

    def put_scenario(self, name: str, **kwargs) -> Scenario:
        json = dict(name=name, **kwargs)
        response = self.actor.put("/scenarios", json=json)
        response.raise_for_status()
        return Scenario.model_validate(response.json())

    def get_scenario(self, name: str = None, id: int = None) -> list[Scenario]:
        params = {"name": name, "id": id}
        params = {k: v for k, v in params.items() if v is not None}
        response = self.actor.get("/scenarios", params=params)
        response.raise_for_status()
        return [Scenario.model_validate(r) for r in response.json()]
