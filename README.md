# CSRS :scissors:

## The CalSim3 Scenario Results Server

A FastAPI-based app to serve results and metadata from multiple CalSim3 model runs. This python package includes clients to ease the interactions with the server.

> [!NOTE]
> This app is under development, currently the target release is 0.1.
> The targeted support is for dashboard clients, so development is focused on relatively fixed data-processing and delivery.
> A secondary support goal is basic data exploration, and Excel compatibility.

## Client Side Usage

Below is a simple example of how to get timeseries data from a remote server if you know the name of the scenario, and the dss path that corresponds to the data.

```python
from csrs.clients import RemoteClient

# Create a client, which handles server interactions and parsing the response
client = RemoteClient("https://www.server_url.com")

# The server stores data using the DSS conventions
dss_path = "/PATH/IN/THE//DSS/FILE"

# Get the data from the srver using the client
timeseries = client.get_timeseries(scenario="Scenario Name", path=dss_path)

# The objects returned have some useful methods.
df = timeseries.to_frame()
```

## Server Side Usage

FastAPI is semi-self documenting, when running the app, the homepage is automatically generated with helpful documentation. As such, this README doesn't repeat that information when possible.

To access that information, run the app locally using `uvicorn`:

```uvicorn csrs.main:app --reload```

The server is designed to be hosted on an Azure WebApp. The deployment of this server is not documented here.
