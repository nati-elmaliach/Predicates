# Predicates
This project provides a Dockerized environment to simplify setup and execution.

## How to run
Build & Run: `docker build -t predicate .` & `docker run predicate remote|tests `

The application accepts one of two modes as an argument:
 - test: Although not strictly necessary, i found it much easier to write tests to validate the logic.
 - remote: Launches a Flask server that responds with a random predicate. Logs are provided to show evaluation results.

## Areas for Improvement
 - **Enhanced Error** Handling: Adding custom error messages would improve readability and debugging.
 - **Additional Tests**: The remote_predicate_resource is currently untested, and there may be some unhandled edge cases.
