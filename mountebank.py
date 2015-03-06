import requests, json

MOUNTEBANK_HOST = 'http://localhost'
MOUNTEBANK_URL = MOUNTEBANK_HOST + ':2525'
IMPOSTERS_URL = MOUNTEBANK_URL + '/imposters'

def create_imposter(definition):
    if isinstance(definition, dict):
        return requests.post(IMPOSTERS_URL, json=definition)
    else:
        return requests.post(IMPOSTERS_URL, data=definition)

def delete_all_imposters():
    return requests.delete(IMPOSTERS_URL)

def delete_imposter(port):
    return requests.delete("{}/imposters/:{}".format(MOUNTEBANK_HOST, port))

def get_all_imposters():
    return requests.get(IMPOSTERS_URL)

def get_imposter(port):
    return requests.get("{}/imposters/:{}".format(MOUNTEBANK_HOST, port))

'''
Imposter has multiple stubs
Stub has multiple predicates and a list of responses
'''

class MountebankException(Exception):
    pass

class Microservice(object):

    def __init__(self, definition):
        resp = create_imposter(definition)
        if resp.status_code != 201:
            raise MountebankException("{}: {}".format(resp.status_code, resp.text))
        self.port = resp.json()['port']

    def get_url(self, *endpoint):
        return "{}:{}{}".format(MOUNTEBANK_HOST, self.port, "".join('/' + name for name in endpoint))

    def get_self(self):
        return get_imposter(self.port)

    def destroy(self):
        return delete_imposter(self.port)


if __name__ == '__main__':
    example_imposter = {
      "protocol": "http",
      "stubs": [{
        "responses": [
          { "is": { "statusCode": 400 }}
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

    assert requests.post(ms.get_url('account_overview'), params={'advertiser': 'a', 'start_date': 'b', 'end_date': 'c'}).status_code == 200
    assert requests.post(ms.get_url('account_overview'), params={'advertiser': 'a', 'start_date': 'b'}).status_code == 400

    ms.destroy()
    delete_al
