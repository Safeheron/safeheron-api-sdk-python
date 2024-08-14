from safeheron_api_sdk_python.tools import *


class WebhookConverter:

    def __init__(self, config):
        self.safeheron_webHook_rsa_public_key = config['safeheronWebHookRsaPublicKey']
        if config.get('webHookRsaPrivateKey'):
            self.web_hook_rsa_private_key = PEM_PRIVATE_HEAD + config['webHookRsaPrivateKey'] + PEM_PRIVATE_END
        if config.get('webHookRsaPrivateKeyPemFile'):
            self.web_hook_rsa_private_key = load_rsa_private_key(config['webHookRsaPrivateKeyPemFile'])

    def converter(self, webhook):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + self.safeheron_webHook_rsa_public_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(self.web_hook_rsa_private_key)
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
        rsaType = ''
        if "rsaType" in webhook:
            rsaType = webhook.pop('rsaType')

        aesType = ''
        if "aesType" in webhook:
            aesType = webhook.pop('aesType')

        sig = webhook.pop('sig')
        need_sign_message = sort_request(webhook)
        v = rsa_verify(platform_rsa_pk, need_sign_message, sig)
        if not v:
            raise Exception("rsa verify: false")

        # 2 get aes key and iv
        key = webhook.pop('key')
        if ECB_OAEP_TYPE == rsaType:
            aes_data = rsa_oaep_decrypt(api_user_rsa_sk, key)
        else:
            aes_data = rsa_decrypt(api_user_rsa_sk, key)
        aes_key = aes_data[0:32]
        aes_iv = aes_data[32:48]

        # 3 aes decrypt data, get response data
        if GCM_TYPE == aesType:
            r = aes_gcm_decrypt(aes_key, aes_iv, b64decode(webhook['bizContent']))
        else:
            r = aes_decrypt(aes_key, aes_iv, b64decode(webhook['bizContent']))
        # response_dict['bizContent'] = json.loads(r.decode())

        return json.loads(r.decode())
