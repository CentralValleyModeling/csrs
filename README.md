# CalSim3 Scenario Server
A FastAPI app to serve CalSim3 input data and results.

> [!NOTE]
> This app is under development, currently the target release is 0.1.
> The targeted support is for dashboard clients, so development is focused on relatively fixed data-processing and delivery. 
> A secondary support goal is basic data exploration, and Excel compatibility. 

## Documentation
FastAPI is semi-self documenting, when running the app, the homepage is automatically generated with helpful documentation. As such, this README doesn't repeat that information when possible.

To access that information, run the app locally using `uvicorn`:

```uvicorn calsim_scenario_server.main:app --reload```