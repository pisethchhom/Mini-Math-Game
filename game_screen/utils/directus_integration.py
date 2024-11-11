import os
import requests

DIRECTUS_API_ENDPOINT = os.getenv("DIRECTUS_API_ENDPOINT")
DIRECTUS_TOKEN = os.getenv("DIRECTUS_TOKEN")

def map_response(response):
    match response.status_code:
        case 200 | 201:
            return [True, 'Success', response.json()]
        case _:
            print(response.json())
            print(response.status_code)
            print("+"*12)
    return [False, 'Unable to fetch data from Directus', response.json()]

def get_request(item, select_fields, filter_q = ''):
    headers = {'Authorization': f"Bearer {DIRECTUS_TOKEN}"}
    url = f"{DIRECTUS_API_ENDPOINT}/items/{item}?fields={','.join(select_fields)}{filter_q}"
    
    response = requests.get(url, headers=headers)
    
    return map_response(response)

def post_request(item, body):
    headers = {'Authorization': f"Bearer {DIRECTUS_TOKEN}"}
    url = f"{DIRECTUS_API_ENDPOINT}/items/{item}"

    response = requests.post(url, headers=headers, json=body)
    
    return map_response(response)

def patch_request(item, body):
    headers = {'Authorization': f"Bearer {DIRECTUS_TOKEN}"}
    url = f"{DIRECTUS_API_ENDPOINT}/items/{item}"
 
    response = requests.patch(url, headers=headers, json=body)
    
    return map_response(response)

