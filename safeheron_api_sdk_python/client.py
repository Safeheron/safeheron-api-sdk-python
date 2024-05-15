from safeheron_api_sdk_python.tools import *


class Client:

    def __init__(self, config):
        self.api_key = config['apiKey']
        self.platform_pub_key = config['safeheronPublicKey']
        self.base_url = config['baseUrl']
        if 'requestTimeout' in config and config['requestTimeout'] is not None and config['requestTimeout'] != '':
            self.requestTimeout = config['requestTimeout'] / 1000
        else:
            self.requestTimeout = 10

        if 'privateKey' in config:
            self.use_private_key = PEM_PRIVATE_HEAD + config['privateKey'] + PEM_PRIVATE_END
        if 'privateKeyPemFile' in config:
            private_key_pem_file = config['privateKeyPemFile']
            if private_key_pem_file is not None and private_key_pem_file != '':
                self.use_private_key = load_rsa_private_key(private_key_pem_file)

    def send_request(self, request, uri):
        req = encrypt_request(self.api_key, request, self.platform_pub_key, self.use_private_key)
        res = self.execution(req, uri)
        res.raise_for_status()
        res = res.json()
        return decrypt_response(res, self.platform_pub_key, self.use_private_key)

    def execution(self, request, uri):
        return requests.post(self.base_url + uri, data=json.dumps(request), headers={"Content-Type": "application/json"},
                             timeout=self.requestTimeout)
