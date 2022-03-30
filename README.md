# Python Client

## About

The client connects to [python_server](https://github.com/aleksandrovpa/python-server) and fetch prices for a preset list of financial instruments

### Deploy

At first define corresponding port in the ./k8s/*.yaml file at server_port varible
Then go to Github Actions and start `Build_and_deploy_to_stage` workflow to run linting, docker build/push and deploy to stage environment.

If you are ready to deploy it to production, run `Deploy_to_prod` workflow

### Metrics

There are several metrics which could help you to monitoring the application on `localhost:8000/metrics` route:

 - `request_success` - Shows count of success requests to server
 - `request_error` - Shows count of error requests to server
 - `request_processing_seconds` - Shows time spent for fetch and store data
 - `request_time_histogram` - Shows histogram for the duration in seconds for fetching data from server

### Healthchecks

The application has a `localhost:8000/health` route for check liveness and readiness status of app