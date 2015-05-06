# Mountebank-Python
Simple bindings to make [Mountebank](http://www.mbtest.org) easier to use from Python

Mountebank is a tool which makes it easier to write tests for [Microservice](http://martinfowler.com/articles/microservices.html) architectures by spawning processes which imitate servers (ie. listening to ports locally and responding to HTTP requests).

## Installation
`npm install -g mountebank --production`

`pip install mountebank-python`

## Usage

An "imposter" is a process which listens on a port (pretending to be a server)

An imposter has multiple "stubs"

A stub has a list of "predicates" and "responses"

Predicates define if a stub matches and incoming HTTP request

When a stub matches it responds with the next response in it's responses list


Run `mb` to start mountebank

In python:
  1. Define your imposters (example given in mountebank.py)
  2. Initialize a microservice object
  3. Make requests to it

Example usage in mountebank.py 
