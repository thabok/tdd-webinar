# Example Repo: Test-driven Development Webinar 
This is the example repo for Test-driven Development webinar (January 2025) including automated tests.

## Model files
The model directory contains all files relevant to the Simulink model:
- **seat_heating_controller.slx** (main model)
- init.m
- seat_heating_control_defineIntEnumTypes.m (called by init.m)

## Test files
The test folder contains the test projects (interactive MIL project for developer testing + MIL/SIL project with full testing capabilities, code coverage, etc.) and a python script to automate the test execution:
- seat_heating_control.epp (MIL project)
- seat_heating_control_converted.epp (MIL/SIL project)
- run_tests.py (script that automates the test steps)


## Automated Tests 
The GitHub Actions [pipeline](../.github/workflows/pipeline.yml) is triggered on pull requests and pushes. It performs the following steps:
- Checkout files: Uses the actions/checkout@v4 action to check out the repository files.
- Build docker image: Builds a Docker image named ep-ml with specific environment variables if the image does not already exist.
- Run tests (docker/linux): Runs tests inside the Docker container using a specified Python script.
- Publish test results to GitHub Pages: Uses the peaceiris/actions-gh-pages@v4 action to publish test results to GitHub Pages.
- Publish results: Uses the dorny/test-reporter@v1 action to publish test results, regardless of success or failure.
- Add test report link to PR: Adds a comment to the pull request with a link to the test report hosted on GitHub Pages.


## Docker
The Dockerfile enabled the tests to be executed without having MATLAB or BTC EmbeddedPlatform installed.
