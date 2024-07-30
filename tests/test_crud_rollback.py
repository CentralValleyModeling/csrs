from typing import Callable

from csrs import crud


def test_crud_wrapped_with_rollback():
    unwrapped = list()
    for module in crud.__all__:
        for func_name in ("create", "read", "update", "delete"):
            func: Callable | None = getattr(module, func_name, None)
            if func is None:  # Module doesn't have that crud operation
                continue
            try:
                func()
            except NotImplementedError:
                # Don't enforce wrapping on unimplemented functions
                continue
            except TypeError:
                pass
            if func_name == func.__name__:
                unwrapped.append((module, func))

    assert (
        len(unwrapped) == 0
    ), "the following functions appear to be unwrapped: " + ", ".join(
        f"`{m.__name__}.{f.__name__}`" for m, f in unwrapped
    )
