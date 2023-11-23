import sys

sys.path.pop(0)
from safeheron_api_sdk_python.tools import *


class WebhookConverter:

    def __init__(self, config):
        global safeheron_webHook_rsa_public_key
        global web_hook_rsa_private_key
        safeheron_webHook_rsa_public_key = config['safeheronWebHookRsaPublicKey']
        if 'webHookRsaPrivateKey' in config:
            web_hook_rsa_private_key = PEM_PRIVATE_HEAD + config['webHookRsaPrivateKey'] + PEM_PRIVATE_END
        if 'webHookRsaPrivateKeyPemFile' in config:
            private_key_pem_file = config['webHookRsaPrivateKeyPemFile']
            if private_key_pem_file is not None and private_key_pem_file != '':
                web_hook_rsa_private_key = load_rsa_private_key(private_key_pem_file)

    def converter(self, webhook):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + safeheron_webHook_rsa_public_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(web_hook_rsa_private_key)
        required_keys = {
            'key',
            'sig',
            'bizContent',
            'timestamp',
        }

        missing_keys = required_keys.difference(webhook.keys())
        if missing_keys:
            raise Exception(webhook)

        # 1 rsa verify
        sig = webhook.pop('sig')
        need_sign_message = sort_request(webhook)
        v = rsa_verify(platform_rsa_pk, need_sign_message, sig)
        if not v:
            raise Exception("rsa verify: false")

        # 2 get aes key and iv
        key = webhook.pop('key')
        aes_data = rsa_decrypt(api_user_rsa_sk, key)
        aes_key = aes_data[0:32]
        aes_iv = aes_data[32:48]

        # 3 aes decrypt data, get response data
        r = aes_decrypt(aes_key, aes_iv, b64decode(webhook['bizContent']))
        # response_dict['bizContent'] = json.loads(r.decode())

        return json.loads(r.decode())
