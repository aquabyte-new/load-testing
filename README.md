# Load Testing

This is the load testing suite for all the cloud applications in Aquabyte. Every service should have its own folder under [`src/load_testing`](https://github.com/aquabyte-new/load-testing/tree/master/src/load_testing).

It uses locust as the underlying tool for writing the load tests. You may want to go over [this Getting Started guide](https://docs.locust.io/en/stable/quickstart.html) (should take ~20-30 minutes) once before diving into the code or writing a new load test.

## Running the load tests

Running the load tests is very simple. Just `cd` into the relevant folder for the service you want to load test and run the command `locust` from the Terminal. For example:

```
source ./.venv/bin/activate
cd ./src/load_testing/isv2
locust
```

**Make sure you are hitting the desired endpoint by checking the source code first! Don't accidentally load test production instead of staging!**


## Initial Development Setup

Run this to create the virtual environment and download data files.
```
make init
```

After this, activate your virtual environment by
```
source .venv/bin/activate
```
