# Tutorials

These tutorials are written to get new users up and running with `csrs`.

## Installation

Conda is the preferred package manager for `csrs` due to certain preferred dependencies. In the future `csrs` may be distributed via PyPI, but not as of now.

### Conda

```powershell
conda install csrs -c dwr-cvm
```

## Basic Usage

The library is used to interact with CalSim results that are stored on a common server. This data is accessable via any HTTP request to the host server. The endpoints and query structure is documented on the root of the server using the auto-created Swagger UI from FastAPI. This package also provides a `RemoteClient` class that helps interact with these servers. Below is an example of how to retrieve data when you know the URL of the server:

```python
import csrs

url = "https://calsim-scenario-results-server.azurewebsites.net"

client = csrs.RemoteClient(url)

timeseries = client.get_timeseries(
    scenrio="Scenario Name",
    version="1.0",
    path="shasta_storage",
)

print(timeseries.values)
```

Check out the [API documentation](api.md) for more information on the methods on the `RemoteClient` class.
