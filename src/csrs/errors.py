from typing import Iterable

from .models import Base


class DuplicateModelError(Exception):
    def __init__(self, model: Base, **duplicate_fields: dict[str, str]):
        error_message = f"{model=} already exists where:\n\t" + "\n\t".join(
            f"{k}: {v}" for k, v in duplicate_fields.items()
        )
        super().__init__(error_message)


class UniqueLookupError(Exception):
    def __init__(self, model: Base, objects: Iterable[Base], **filters):
        error_message = (
            f"{len(objects)} {model.__name__} were found when 1 was expected,\n"
            + " filters were:\n\t"
            + "\n\t".join(f"{k}: {v}" for k, v in filters.items())
        )
        if len(objects) > 0:
            error_message = error_message + "\nthe objects were:" + "\n\t".join(objects)

        super().__init__(error_message)
