# Mountebank-Python
Simple bindings to make [Mountebank](http://www.mbtest.org) easier to use from Python
Mountebank is a tool which makes it easier to write tests for [Microservice](http://martinfowler.com/articles/microservices.html) architectures by spawning processes which imitate servers locally.

## Installation
`npm install -g mountebank --production`

`pip install mountebank-python`

## Usage

Imposter - A process which listens on a port (pretending to be a server)
Imposter has multiple stubs
A stub has multiple "predicates" and "responses"
Predicates define which stub matches
when a stub matches it uses its next response

Run `mb` to start mountebank

In python:
  1. Define your imposters (example given in mountebank.py)
  2. Initialize a microservice object
  3. Make requests to it

Example usage in mountebank.py 
