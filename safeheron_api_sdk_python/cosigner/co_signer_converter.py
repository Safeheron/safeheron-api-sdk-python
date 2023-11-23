import sys

sys.path.pop(0)
from safeheron_api_sdk_python.tools import *


class CoSignerResponse:
    def __init__(self):
        # approve
        self.approve = None
        # txKey
        self.txKey = None


class CoSignerConverter:

    def __init__(self, config):
        global api_pub_key
        global biz_privKey
        api_pub_key = config['apiPubKey']
        if 'bizPrivKey' in config:
            biz_privKey = PEM_PRIVATE_HEAD + config['bizPrivKey'] + PEM_PRIVATE_END
        if 'bizPrivKeyPemFile' in config:
            private_key_pem_file = config['bizPrivKeyPemFile']
            if private_key_pem_file is not None and private_key_pem_file != '':
                biz_privKey = load_rsa_private_key(private_key_pem_file)

    def request_convert(self, co_signer_call_back):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + api_pub_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(biz_privKey)
        required_keys = {
            'key',
            'sig',
            'bizContent',
            'timestamp',
        }

        missing_keys = required_keys.difference(co_signer_call_back.keys())
        if missing_keys:
            raise Exception(co_signer_call_back)

        # 1 rsa verify
        sig = co_signer_call_back.pop('sig')
        need_sign_message = sort_request(co_signer_call_back)
        v = rsa_verify(platform_rsa_pk, need_sign_message, sig)
        if not v:
            raise Exception("rsa verify: false")

        # 2 get aes key and iv
        key = co_signer_call_back.pop('key')
        aes_data = rsa_decrypt(api_user_rsa_sk, key)
        aes_key = aes_data[0:32]
        aes_iv = aes_data[32:48]

        # 3 aes decrypt data, get response data
        r = aes_decrypt(aes_key, aes_iv, b64decode(co_signer_call_back['bizContent']))
        # response_dict['bizContent'] = json.loads(r.decode())

        return json.loads(r.decode())

    def response_converter(self, co_signer_response: CoSignerResponse):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + api_pub_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(PEM_PRIVATE_HEAD + biz_privKey + PEM_PRIVATE_END)

        ret = dict()

        # prepare aes key and iv
        aes_key = get_random_bytes(32)
        aes_iv = get_random_bytes(16)
        response_data = json.dumps(co_signer_response.__dict__).replace('\'', '\"').replace('\n', '').encode('utf-8')

        # 1 rsa encrypt aes key + iv
        aes_data = aes_key + aes_iv
        ret['key'] = rsa_encrypt(platform_rsa_pk, aes_data)

        # 2 aes encrypt request data
        if response_data is not None:
            aes_encrypted_bytes = aes_encrypt(aes_key, aes_iv, response_data)
            ret['bizContent'] = b64encode(aes_encrypted_bytes).decode()

        # 3 set timestamp
        ret['timestamp'] = str(int(time.time() * 1000))
        ret['code'] = str('200')
        ret['message'] = str('SUCCESS')

        # 4 sign request
        need_sign_message = sort_request(ret)
        ret['sig'] = rsa_sign(api_user_rsa_sk, need_sign_message)

        return ret
