import requests, json

URL = 'http://localhost:2525'

def create_imposter(json_blob):
	requests.post(URL + '/imposters', json=json_blob)

def delete_all_imposters():
	return requests.delete(URL + '/imposters')

def get_all_imposters():
	return requests.get(URL + '/imposters')

'''
Imposter has multiple stubs
Stub has multiple predicates and a list of responses
'''