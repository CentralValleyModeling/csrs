from csrs import clients, schemas


def test_local_standard_paths(client_local: clients.LocalClient):
    # We only test this one with the local client, since during tests we are only
    # accessing one local database. The unique constraint on the database would cause
    # the second test to fail since the first test adds the paths to the database
    paths = client_local.put_standard_paths()
    assert len(paths) > 0
    assert isinstance(paths[0], schemas.NamedPath)

    array = client_local.get_path(
        path=paths[0].path,
    )
    assert len(array) == 1
    assert array[0].detail == paths[0].detail
