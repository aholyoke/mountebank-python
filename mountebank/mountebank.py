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
        resp = create_imposter(definition)
        if resp.status_code != 201:
            raise MountebankException("{}: {}".format(resp.status_code, resp.text))
        self.port = resp.json()['port']

    def get_url(self, *endpoint):
        return "{}:{}/{}".format(MOUNTEBANK_HOST, self.port, "/".join(name for name in endpoint))

    def get_self(self):
        return get_imposter(self.port)

    def destroy(self):
        return delete_imposter(self.port)


class MicroserviceArchitecture(object):
    def __init__(self, definitions):
        resp = create_all_imposters(definitions)
        if resp.status_code != 200:
            raise MountebankException("{}: {}".format(resp.status_code, resp.text))
        self.ports = [imp['port'] for imp in resp.json()['imposters']]

    def get_url(self, port, *endpoint):
        return "{}:{}/{}".format(MOUNTEBANK_HOST, port, "/".join(name for name in endpoint))

    def get_self(self, port):
        return get_imposter(port)

    def destroy(self, port):
        return delete_imposter(port)

    def destroy_all(self):
        delete_all_imposters()


if __name__ == '__main__':
    example_imposter = {
      "protocol": "http",
      "stubs": [{
        "responses": [
          {"is": {"statusCode": 400}}
        ],
        "predicates": [{
          "and": [
            {
              "equals": {
                "path": "/account_overview",
                "method": "POST"
              }
            },
            {
              "not": {
                "exists": {
                  "query": {
                    "advertiser": True,
                    "start_date": True,
                    "end_date": True
                  }
                },
                "caseSensitive": True
              }
            }
          ]
        }]
      }]
    }
    ms = Microservice(example_imposter)

    r1 = requests.post(ms.get_url('account_overview'), params={'advertiser': 'a', 'start_date': 'b', 'end_date': 'c'})
    r2 = requests.post(ms.get_url('account_overview'), params={'advertiser': 'a', 'start_date': 'b'})
    assert r1.status_code == 200
    assert r2.status_code == 400

    ms.destroy()
    delete_all_imposters()

    example_architecture = {
        "imposters": [
            {
                "protocol": "http",
                "port": 4546,
                "stubs": [{
                    "responses": [{"is": {"statusCode": 400}}],
                    "predicates": [{
                        "equals": {
                            "path": "/a/b",
                            "method": "POST"
                        }
                    }]
                }],
            },
            {
                "protocol": "http",
                "port": 4547,
                "mode": "binary"
            },
            {
                "protocol": "smtp",
                "port": 4548
            }
        ]
    }
    # are we webscale yet?
    msa = MicroserviceArchitecture(example_architecture)
    r1 = requests.post(msa.get_url(4546, 'a', 'b'))
    r2 = requests.put(msa.get_url(4546, 'a', 'b'))
    r3 = requests.post(msa.get_url(4546, 'a'))
    r4 = requests.post(msa.get_url(4547, 'a'))
    assert r1.status_code == 400
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert r4.status_code == 200
