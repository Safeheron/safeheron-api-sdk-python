from safeheron_api_sdk_python.tools import *


class CoSignerResponse:
    def __init__(self):
        # approve
        self.approve = None
        # txKey
        self.txKey = None


class CoSignerConverter:

    def __init__(self, config):
        self.api_pub_key = config['apiPubKey']
        if config.get('bizPrivKey'):
            self.biz_privKey = PEM_PRIVATE_HEAD + config['bizPrivKey'] + PEM_PRIVATE_END
        if config.get('bizPrivKeyPemFile'):
            self.biz_privKey = load_rsa_private_key(config['bizPrivKeyPemFile'])

    def request_convert(self, co_signer_call_back):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + self.api_pub_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(self.biz_privKey)
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
        rsaType = ''
        if "rsaType" in co_signer_call_back:
            rsaType = co_signer_call_back.pop('rsaType')

        aesType = ''
        if "aesType" in co_signer_call_back:
            aesType = co_signer_call_back.pop('aesType')

        sig = co_signer_call_back.pop('sig')
        need_sign_message = sort_request(co_signer_call_back)
        v = rsa_verify(platform_rsa_pk, need_sign_message, sig)
        if not v:
            raise Exception("rsa verify: false")

        # 2 get aes key and iv
        key = co_signer_call_back.pop('key')
        if ECB_OAEP_TYPE == rsaType:
            aes_data = rsa_oaep_decrypt(api_user_rsa_sk, key)
        else:
            aes_data = rsa_decrypt(api_user_rsa_sk, key)
        aes_key = aes_data[0:32]
        aes_iv = aes_data[32:48]

        # 3 aes decrypt data, get response data
        if GCM_TYPE == aesType:
            r = aes_gcm_decrypt(aes_key, aes_iv, b64decode(co_signer_call_back['bizContent']))
        else:
            r = aes_decrypt(aes_key, aes_iv, b64decode(co_signer_call_back['bizContent']))
        # response_dict['bizContent'] = json.loads(r.decode())

        return json.loads(r.decode())

    # It has been Deprecated,Please use convertCoSignerResponseWithNewCryptoType
    def response_converter(self, co_signer_response: CoSignerResponse):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + self.api_pub_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(self.biz_privKey)

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

    def response_converter_with_new_crypto_type(self, co_signer_response: CoSignerResponse):
        platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + self.api_pub_key + PEM_PUBLIC_END)
        api_user_rsa_sk = get_rsa_key(self.biz_privKey)

        ret = dict()

        # prepare aes key and iv
        aes_key = get_random_bytes(32)
        aes_iv = get_random_bytes(16)
        response_data = json.dumps(co_signer_response.__dict__).replace('\'', '\"').replace('\n', '').encode('utf-8')

        # 1 rsa encrypt aes key + iv
        aes_data = aes_key + aes_iv
        ret['key'] = rsa_oaep_encrypt(platform_rsa_pk, aes_data)

        # 2 aes encrypt request data
        if response_data is not None:
            aes_encrypted_bytes = aes_gcm_encrypt(aes_key, aes_iv, response_data)
            ret['bizContent'] = b64encode(aes_encrypted_bytes).decode()

        # 3 set timestamp
        ret['timestamp'] = str(int(time.time() * 1000))
        ret['code'] = str('200')
        ret['message'] = str('SUCCESS')

        # 4 sign request
        need_sign_message = sort_request(ret)
        ret['sig'] = rsa_sign(api_user_rsa_sk, need_sign_message)
        ret['rsaType'] = ECB_OAEP_TYPE
        ret['aesType'] = GCM_TYPE
        return ret
