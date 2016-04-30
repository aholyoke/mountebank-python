import requests
import json
'''
http://www.mbtest.org/
imposter has multiple stubs
stub has multiple predicates and responses
predicates define which stub matches
when a stub matches it uses its next response
'''

MOUNTEBANK_HOST = 'http://localhost'
MOUNTEBANK_URL = MOUNTEBANK_HOST + ':2525'
IMPOSTERS_URL = MOUNTEBANK_URL + '/imposters'


def create_imposter(definition, method='POST'):
    if isinstance(definition, dict):
        return requests.request(method, IMPOSTERS_URL, json=definition)
    else:
        return requests.request(method, IMPOSTERS_URL, data=definition)


def create_all_imposters(definitions):
    """ PUTting a list of definitions to the imposter endpoint creates imposters in bulk"""
    return create_imposter(definitions, 'PUT')


def delete_all_imposters():
    return requests.delete(IMPOSTERS_URL)


def delete_imposter(port):
    return requests.delete("{}/imposters/{}".format(MOUNTEBANK_URL, port))


def get_all_imposters():
    return requests.get(IMPOSTERS_URL)


def get_imposter(port):
    return requests.get("{}/imposters/{}".format(MOUNTEBANK_URL, port))


class MountebankException(Exception):
    pass


class Microservice(object):
    def __init__(self, definition):
        self.definition = definition

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return "Microservice(port={})".format(self.port)

    def start(self):
        resp = create_imposter(self.definition)
        if resp.status_code != 201:
            raise MountebankException("{}: {}".format(resp.status_code, resp.text))
        self.port = resp.json()['port']
        return self

    def stop(self):
        return self.destroy()

    def get_url(self, *endpoint):
        return "{}:{}/{}".format(MOUNTEBANK_HOST, self.port, "/".join(name for name in endpoint))

    def get_self(self):
        return get_imposter(self.port)

    def destroy(self):
        return delete_imposter(self.port)


class MicroserviceArchitecture(object):
    def __init__(self, definitions):
        self.definitions = definitions

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def __repr__(self):
        return "MicroserviceArchitecture(ports={})".format(self.ports)

    def start(self):
        resp = create_all_imposters(self.definitions)
        if resp.status_code != 200:
            raise MountebankException("{}: {}".format(resp.status_code, resp.text))
        self.ports = [imp['port'] for imp in resp.json()['imposters']]

    def stop(self):
        return [self.destroy(port) for port in self.ports]

    def get_url(self, port, *endpoint):
        return "{}:{}/{}".format(MOUNTEBANK_HOST, port, "/".join(name for name in endpoint))

    def get_urls(self):
        return [self.get_url(port) for port in self.ports]

    def get_self(self, port):
        return get_imposter(port)

    def get_selves(self):
        return [self.get_self(port) for port in self.ports]

    def destroy(self, port):
        return delete_imposter(port)

    def destroy_all(self):
        delete_all_imposters()
