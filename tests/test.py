from mountebank import Microservice, MicroserviceArchitecture, delete_all_imposters
import requests
import unittest


class TestMicroservice(unittest.TestCase):
    def setUp(self):
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
                    "path": "/overview",
                    "method": "POST"
                  }
                },
                {
                  "not": {
                    "exists": {
                      "query": {
                        "param1": True,
                        "param2": True,
                        "param3": True
                      }
                    },
                    "caseSensitive": True
                  }
                }
              ]
            }]
          }]
        }
        self.ms = Microservice(example_imposter)

    def test_required_params(self):
        r1 = requests.post(
            self.ms.get_url('overview'),
            params={'param1': 'a', 'param2': 'b', 'param3': 'c'})
        r2 = requests.post(
            self.ms.get_url('overview'),
            params={'param1': 'a', 'param2': 'b'})
        self.assertEqual(r1.status_code, 200)
        self.assertEqual(r2.status_code, 400)

    def tearDown(self):
        self.ms.destroy()
        delete_all_imposters()


class TestMicroserviceArchitecture(unittest.TestCase):
    def setUp(self):
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
                },
                {
                    "protocol": "smtp",
                    "port": 4548
                }
            ]
        }
        # are we webscale yet?
        self.msa = MicroserviceArchitecture(example_architecture)

    def test_required_params(self):
        r1 = requests.post(self.msa.get_url(4546, 'a', 'b'))
        r2 = requests.put(self.msa.get_url(4546, 'a', 'b'))
        r3 = requests.post(self.msa.get_url(4546, 'a'))
        r4 = requests.post(self.msa.get_url(4547, 'a'))
        self.msa.destroy(4546)

        self.assertEqual(r1.status_code, 400)
        self.assertEqual(r2.status_code, 200)
        self.assertEqual(r3.status_code, 200)
        self.assertEqual(r4.status_code, 200)

    def tearDown(self):
        self.msa.destroy_all()


if __name__ == '__main__':
    unittest.main()
