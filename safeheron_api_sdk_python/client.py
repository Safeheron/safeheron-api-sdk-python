from safeheron_api_sdk_python.tools import *

class Client:

    def __init__(self, config):
        global api_key
        global platform_pub_key
        global use_private_key
        global base_url
        api_key = config['apiKey']
        platform_pub_key = config['safeheronPublicKey']
        use_private_key = config['privateKey']
        base_url = config['baseUrl']

    def send_request(self, request, uri):
        req = encrypt_request(api_key, request, platform_pub_key, use_private_key)
        res = self.execution(req, uri)
        res.raise_for_status()
        res = res.json()
        return decrypt_response(res, platform_pub_key, use_private_key)

    def execution(self, request, uri):
        return requests.post(base_url + uri, data=json.dumps(request), headers={"Content-Type": "application/json"})
