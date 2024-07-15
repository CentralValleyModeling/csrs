from typing import Iterable


class DuplicateAssumptionError(Exception):
    def __init__(self, on_name: bool, on_detail: bool):
        super().__init__(
            "assumption given is a duplicate,\n"
            + f"\tduplicate name={on_name},\n"
            + f"\tduplicate detail={on_detail}."
        )


class DuplicateScenarioError(Exception):
    def __init__(self, name: str):
        super().__init__("scenario given is a duplicate,\n\tduplicate {name=}.")


class LookupUniqueError(Exception):
    def __init__(self, model, returned, **filters):
        if hasattr(returned, "__iter__"):
            returned = len(returned)

        super().__init__(
            f"couldn't find unique entry in {model} table for filters given,\n"
            + f"\titems found: {returned}\n"
            + "\tfilters:\n\t\t"
            + "\n\t\t".join(f"{k}: {v}" for k, v in filters.items())
        )


class ScenarioAssumptionError(Exception):
    def __init__(self, missing: Iterable[str] = None, extra: Iterable[str] = None):
        super().__init__(
            "the scenario was not correctly given assumptions:\n"
            + f"\t{missing=}\n"
            + f"\t{extra=}.",
        )
