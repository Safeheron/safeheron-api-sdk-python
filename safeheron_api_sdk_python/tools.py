# Crypto 可直接替换为 Cryptodome
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from base64 import b64encode, b64decode
from Cryptodome.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
from Cryptodome.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Cryptodome.Hash import SHA256, SHA1
from Cryptodome import Random
import json
import time
import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


PEM_PUBLIC_HEAD = "-----BEGIN PUBLIC KEY-----\n"
PEM_PUBLIC_END = "\n-----END PUBLIC KEY-----"
PEM_PRIVATE_HEAD = "-----BEGIN RSA PRIVATE KEY-----\n"
PEM_PRIVATE_END = "\n-----END RSA PRIVATE KEY-----"

def load_rsa_private_key(file_path, password=None):
    try:
        with open(file_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=password,
                backend=default_backend()
            )
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        return pem.decode()
    except Exception as e:
        raise Exception("Failed to parse rsa pem file")

def check_key_and_iv(key: bytes, iv: bytes):
    if len(key) != 32:
        raise Exception("aes error: key must have 32 bytes")
    if len(iv) != 16:
        raise Exception("aes error: iv must have 16 bytes")


def aes_encrypt(key: bytes, iv: bytes, message: bytes):
    check_key_and_iv(key, iv)
    message = pad(message, AES.block_size)
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypt_text = cipher.encrypt(message)
    except Exception as e:
        raise Exception("aes encrypt error: %s" % e)
    return encrypt_text


def aes_decrypt(key: bytes, iv: bytes, encrypt_text: bytes):
    check_key_and_iv(key, iv)
    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pad_text = cipher.decrypt(encrypt_text)
    except Exception as e:
        raise Exception("aes decrypt error: %s" % e)
    return unpad(pad_text, AES.block_size)


def get_rsa_key(key_pem, passphrase=None):
    if key_pem == '':
        raise Exception("rsa encrypt error: pubkey can't be none")
    if passphrase is None:
        return RSA.import_key(key_pem)
    else:
        return RSA.import_key(key_pem, passphrase=passphrase)


def rsa_encrypt(public_key, message: bytes):
    try:
        cipher_rsa = Cipher_pkcs1_v1_5.new(public_key)
        encrypt_text = cipher_rsa.encrypt(message)
    except Exception as e:
        raise Exception("rsa encrypt error: %s" % e)
    encrypt_text_base64 = b64encode(encrypt_text)
    return encrypt_text_base64.decode('utf-8')


def rsa_decrypt(private_key, message: str):
    encrypt_text = b64decode(message)
    try:
        cipher_rsa = Cipher_pkcs1_v1_5.new(private_key)
        sentinel = Random.new().read(SHA1.digest_size)
        return cipher_rsa.decrypt(encrypt_text, sentinel)
    except Exception as e:
        raise Exception("rsa decrypt error: %s" % e)


def rsa_sign(private_key, message_hash: bytes):
    try:
        signer = Signature_pkcs1_v1_5.new(private_key)
        digest = SHA256.new()
        digest.update(message_hash)
        signed = signer.sign(digest)
        return b64encode(signed).decode()
    except Exception as e:
        raise Exception("rsa sign error: %s" % e)


def rsa_verify(public_key, message_hash: bytes, signature):
    try:
        signer = Signature_pkcs1_v1_5.new(public_key)
        digest = SHA256.new()
        digest.update(message_hash)
        return signer.verify(digest, b64decode(signature))
    except Exception as e:
        raise Exception("rsa sign error: %s" % e)


def sort_request(r: dict):
    sortData = json.dumps(r, sort_keys=True).replace(' ', '')
    strArr = []
    data1 = json.loads(sortData)
    for key, value in data1.items():
        # print(value, type(value))
        if isinstance(value, dict):  # 注意：对于dict类型的数据，一定要保留双引号，但python默认都是单引号
            val = json.dumps(value).replace(' ', '')
        else:
            val = value
        strArr.append(key + '=' + str(val))
    return "&".join(strArr).encode('utf-8')


def encrypt_request(api_key, request_dict, platform_rsa_pk, api_user_rsa_sk):
    platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + platform_rsa_pk + PEM_PUBLIC_END)
    api_user_rsa_sk = get_rsa_key(api_user_rsa_sk)

    ret = dict()

    ret['apiKey'] = api_key

    # prepare aes key and iv
    aes_key = get_random_bytes(32)
    aes_iv = get_random_bytes(16)


    # 1 rsa encrypt aes key + iv
    aes_data = aes_key + aes_iv
    ret['key'] = rsa_encrypt(platform_rsa_pk, aes_data)

    # 2 aes encrypt request data
    if request_dict is not None:
        request_data = json.dumps(request_dict.__dict__).replace('\'', '\"').replace('\n', '').encode('utf-8')
        aes_encrypted_bytes = aes_encrypt(aes_key, aes_iv, request_data)
        ret['bizContent'] = b64encode(aes_encrypted_bytes).decode()

    # 3 set timestamp
    ret['timestamp'] = str(int(time.time() * 1000))

    # 4 sign request
    need_sign_message = sort_request(ret)
    ret['sig'] = rsa_sign(api_user_rsa_sk, need_sign_message)

    return ret


def decrypt_response(response_dict, platform_rsa_pk, api_user_rsa_sk):
    platform_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + platform_rsa_pk + PEM_PUBLIC_END)
    api_user_rsa_sk = get_rsa_key(api_user_rsa_sk)
    required_keys = {
        'key',
        'sig',
        'bizContent',
        'timestamp',
        'code',
        'message'
    }
    missing_keys = required_keys.difference(response_dict.keys())
    if missing_keys:
        raise Exception(response_dict)

    # 1 rsa verify
    sig = response_dict.pop('sig')
    need_sign_message = sort_request(response_dict)
    v = rsa_verify(platform_rsa_pk, need_sign_message, sig)
    if not v:
        raise Exception("rsa verify: false")

    # 2 get aes key and iv
    key = response_dict.pop('key')
    aes_data = rsa_decrypt(api_user_rsa_sk, key)
    aes_key = aes_data[0:32]
    aes_iv = aes_data[32:48]

    # 3 aes decrypt data, get response data
    r = aes_decrypt(aes_key, aes_iv, b64decode(response_dict['bizContent']))
    #response_dict['bizContent'] = json.loads(r.decode())

    return json.loads(r.decode())

#Used for webhook decryption callback request data
def decrypt_request(response_dict, verify_rsa_pk, decrypt_rsa_sk):
    verify_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + verify_rsa_pk + PEM_PUBLIC_END)
    decrypt_rsa_sk = get_rsa_key(decrypt_rsa_sk)
    # 1 rsa verify
    sig = response_dict.pop('sig')
    need_sign_message = sort_request(response_dict)
    v = rsa_verify(verify_rsa_pk, need_sign_message, sig)
    if not v:
        raise Exception("rsa verify: false")

    # 2 get aes key and iv
    aes_data = rsa_decrypt(decrypt_rsa_sk, response_dict['key'])
    aes_key = aes_data[0:32]
    aes_iv = aes_data[32:48]
  
    # 3 aes decrypt data, get response data
    r = aes_decrypt(aes_key, aes_iv, b64decode(response_dict['bizContent']))

    return json.loads(r.decode())

#For webhook to send encrypted response content
def encrypt_response(raw_data,encrpyt_rsa_pk, sign_rsa_sk):
    encrpyt_rsa_pk = get_rsa_key(PEM_PUBLIC_HEAD + encrpyt_rsa_pk + PEM_PUBLIC_END)
    sign_rsa_sk = get_rsa_key(sign_rsa_sk)
    ret = dict()
    # prepare aes key and iv
    aes_key = get_random_bytes(32)
    aes_iv = get_random_bytes(16)
    res_data = json.dumps(raw_data).replace('\n', '').encode('utf-8')

    # 1 rsa encrypt aes key + iv
    aes_data = aes_key + aes_iv
    ret['key'] = rsa_encrypt(encrpyt_rsa_pk, aes_data)

    # 2 aes encrypt request data
    aes_encrypted_bytes = aes_encrypt(aes_key, aes_iv, res_data)
    ret['bizContent'] = b64encode(aes_encrypted_bytes).decode()

    # 3 set timestamp , no need to add
    ret['timestamp'] = str(int(time.time() * 1000))

    # 4 code
    ret['code'] = "200"

    # 5 message
    ret['message'] = "callback_ok"

    # 6 sign request
    need_sign_message = sort_request(ret)
    ret['sig'] = rsa_sign(sign_rsa_sk, need_sign_message)
    return ret

def rsa_gen_key():
    rsa_key = RSA.generate(4096)
    sk = rsa_key.export_key()
    pk = rsa_key.publickey().export_key()
    return sk, pk
