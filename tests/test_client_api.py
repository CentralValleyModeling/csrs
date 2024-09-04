import inspect
import logging

from csrs import clients

logger = logging.getLogger(__name__)


def test_base_annotations():
    for name, value in inspect.getmembers(clients.Client, inspect.isfunction):
        if name.startswith("__"):
            continue
        annotations = inspect.get_annotations(value)
        signature = inspect.signature(value)
        expected = len(
            [p for p in signature.parameters if p not in ("self", "args", "kwargs")]
        )
        seen = len({k for k in annotations if k != "return"})
        assert seen == expected, f"clients.Client.{name} isn't fully annotated"
        assert "return" in annotations, f"clients.Client.{name} return isn't annotated"


def test_stub_methods_redefined():
    for name, base_method in inspect.getmembers(clients.Client, inspect.isfunction):
        for child in (clients.LocalClient, clients.RemoteClient):
            child_method = getattr(child, name)
            if child_method.__class__ != base_method.__class__:
                # Only enforce if the method is overwritten in a sub-class
                assert inspect.getsource(child_method) != inspect.getsource(base_method)


def test_remote_vs_local_api():
    compare = (
        (clients.LocalClient, clients.RemoteClient),
        (clients.RemoteClient, clients.LocalClient),
    )
    for left, right in compare:
        for name, left_method in inspect.getmembers(left, inspect.isfunction):
            if name in ("__init__", "close"):
                continue
            right_method = getattr(right, name)
            # If the left method is using base.Client's implementation, they both should
            if left_method.__class__ != left:
                assert (
                    left_method.__class__ == right_method.__class__
                ), f"signatures don't match for {name}"
            # Both methods should have the exact same signature
            left_sig = inspect.signature(left_method)
            right_sig = inspect.signature(right_method)
            assert left_sig == right_sig
