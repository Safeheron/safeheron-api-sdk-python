from safeheron_api_sdk_python.tools import *

class Client:

    def __init__(self, config):
        global api_key
        global platform_pub_key
        global use_private_key
        global base_url
        api_key = config['apiKey']
        platform_pub_key = config['safeheronPublicKey']
        base_url = config['baseUrl']
        if 'privateKey' in config:
            use_private_key = PEM_PRIVATE_HEAD + config['privateKey'] + PEM_PRIVATE_END
        if 'privateKeyPemFile' in config:
            private_key_pem_file = config['privateKeyPemFile']
            if private_key_pem_file is not None and private_key_pem_file != '':
                use_private_key = load_rsa_private_key(private_key_pem_file)

    def send_request(self, request, uri):
        req = encrypt_request(api_key, request, platform_pub_key, use_private_key)
        res = self.execution(req, uri)
        res.raise_for_status()
        res = res.json()
        return decrypt_response(res, platform_pub_key, use_private_key)

    def execution(self, request, uri):
        return requests.post(base_url + uri, data=json.dumps(request), headers={"Content-Type": "application/json"})
