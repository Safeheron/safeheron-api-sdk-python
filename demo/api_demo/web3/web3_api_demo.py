import yaml
from safeheron.api.web3_api import *
from web3 import Web3

import uuid
from eth_account._utils.legacy_transactions import (
    UnsignedTransaction,
    encode_transaction,
    serializable_unsigned_transaction_from_dict, Transaction,
)
from eth_account._utils.typed_transactions import TypedTransaction


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def to_eth_v(v_raw, chain_id=None):
    CHAIN_ID_OFFSET = 35
    V_OFFSET = 27
    if chain_id is None:
        v = v_raw + V_OFFSET
    else:
        v = v_raw + CHAIN_ID_OFFSET + 2 * chain_id
    return v


def big_endian_to_int(value):
    return int.from_bytes(value, 'big')


def get_v_r_s_from_sig(sig, chain_id=None):
    sig_b = bytes.fromhex(sig)
    r = sig_b[0:32]
    s = sig_b[32:64]
    v = sig_b[64]
    r = big_endian_to_int(r)
    s = big_endian_to_int(s)
    v = int(v)
    v = to_eth_v(v, chain_id)
    return v, r, s


def raw_v_r_s_from_sig(sig):
    sig_b = bytes.fromhex(sig)
    r = sig_b[0:32]
    s = sig_b[32:64]
    v = sig_b[64]
    r = big_endian_to_int(r)
    s = big_endian_to_int(s)
    v = int(v)
    return v, r, s


def combine_unsigned_transaction_and_sig(transaction_dict, sig):
    unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction_dict)
    if isinstance(unsigned_transaction, UnsignedTransaction):
        chain_id = None
        (v, r, s) = get_v_r_s_from_sig(sig, chain_id)
    elif isinstance(unsigned_transaction, Transaction):
        chain_id = unsigned_transaction.v
        (v, r, s) = get_v_r_s_from_sig(sig, chain_id)
    elif isinstance(unsigned_transaction, TypedTransaction):
        # Each transaction type dictates its payload, and consequently,
        # all the funky logic around the `v` signature field is both obsolete && incorrect.
        # We want to obtain the raw `v` and delegate to the transaction type itself.
        (v, r, s) = raw_v_r_s_from_sig(sig)
    else:
        # Cannot happen, but better for code to be defensive + self-documenting.
        raise TypeError("unknown Transaction object: %s" % type(unsigned_transaction))

    encoded_transaction = encode_transaction(unsigned_transaction, vrs=(v, r, s))
    return encoded_transaction


def retrieveSig(web3_api, tx_key):
    i = 1
    while i <= 100:
        i += 1
        queryParam = OneWeb3SignRequest()
        queryParam.txKey = tx_key
        one = web3_api.oneWeb3Sign(queryParam)
        print('sign status:', one['transactionStatus'])
        if one['transactionStatus'] == 'SIGN_COMPLETED':
            return one
        time.sleep(5)


class TestWeb3:

    def test_web3_eth_sign(self):
        config = read_yaml("./config.yaml")
        # EVM
        py_web3 = Web3(Web3.HTTPProvider(config['ethereumRpcApi']))
        # erc20ContractAddress
        token_address = config['erc20ContractAddress']
        # accountTokenAddress
        sender_address = config['accountTokenAddress']
        # toAddress
        recipient_address = config['toAddress']
        # amount
        amount = 1
        # nonce
        nonce = py_web3.eth.get_transaction_count(sender_address)
        # decimals
        decimals = 18
        # amount_in_wei
        amount_in_wei = amount * 10 ** decimals
        transfer_function_signature = 'transfer(address,uint256)'
        data = py_web3.to_hex(py_web3.keccak(text=transfer_function_signature)[:4] +
                              py_web3.to_bytes(hexstr=recipient_address[2:].zfill(64)) +
                              amount_in_wei.to_bytes(32, byteorder='big'))
        gas_limit = py_web3.eth.estimate_gas({
            'to': token_address,
            'from': sender_address,
            'data': data,
        })
        # Get the latest block information
        latest_block = py_web3.eth.get_block('latest')
        # Estimate maxFeePerGas, we assume maxPriorityFeePerGas's value is 2(gwei)
        max_priority_fee_per_gas = py_web3.to_wei(2, "gwei")
        base_fee_per_gas = latest_block['baseFeePerGas']
        # The baseFeePerGas is recommended to be 2 times the latest block's baseFeePerGas value
        # maxFeePerGas must not less than baseFeePerGas + maxPriorityFeePerGas
        max_fee_per_gas = base_fee_per_gas * 2 + max_priority_fee_per_gas

        transaction = {
            'nonce': nonce,
            'to': token_address,
            'data': data,
            'value': 0,
            'chainId': py_web3.eth.chain_id,
            'gas': gas_limit,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'maxFeePerGas': max_fee_per_gas
        }
        unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction)
        transaction_hash = unsigned_transaction.hash()

        web3_api = Web3Api(config)
        param = CreateWeb3EthSignRequest()
        param.accountKey = config['accountKey']
        param.customerRefId = str(uuid.uuid1())
        param.messageHash.chainId = transaction['chainId']
        param.messageHash.hash = [transaction_hash.hex()]

        res = web3_api.createWeb3EthSign(param)
        txKey = res['txKey']
        print(txKey)
        sig = retrieveSig(web3_api, txKey)['messageHash']['sigList'][0]['sig']
        signed_raw_transaction = combine_unsigned_transaction_and_sig(transaction, sig)
        print('signed_raw_transaction', signed_raw_transaction.hex())
        tx_hash = py_web3.eth.send_raw_transaction(signed_raw_transaction.hex()).hex()
        print('tx_hash', tx_hash)

    def test_web3_personal_sign(delf):
        config = read_yaml("./config.yaml")
        py_web3 = Web3(Web3.HTTPProvider(config['ethereumRpcApi']))
        web3_api = Web3Api(config)
        param = CreateWeb3PersonalSignRequest()
        param.accountKey = config['accountKey']
        param.customerRefId = str(uuid.uuid1())
        param.message.chainId = py_web3.eth.chain_id
        param.message.data = 'demo text'
        res = web3_api.createWeb3PersonalSign(param)
        txKey = res['txKey']
        print(txKey)
        sig = retrieveSig(web3_api, txKey)['message']['sig']['sig']
        print('sig', sig)

    def test_web3_eth_sign_typed_data(delf):
        config = read_yaml("./config.yaml")
        py_web3 = Web3(Web3.HTTPProvider(config['ethereumRpcApi']))

        web3_api = Web3Api(config)
        param = CreateWeb3EthSignTypedDataRequest()
        param.accountKey = config['accountKey']
        param.customerRefId = str(uuid.uuid1())
        param.message.chainId = py_web3.eth.chain_id
        param.message.data = '{"types":{"EIP712Domain":[{"name":"name","type":"string"},{"name":"version","type":"string"},{"name":"chainId","type":"uint256"},{"name":"verifyingContract","type":"address"}],"Person":[{"name":"name","type":"string"},{"name":"wallet","type":"address"}],"Mail":[{"name":"from","type":"Person"},{"name":"to","type":"Person"},{"name":"contents","type":"string"}]},"primaryType":"Mail","domain":{"name":"Ether Mail","version":"1","chainId":1,"verifyingContract":"0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC"},"message":{"from":{"name":"Cow","wallet":"0xCD2a3d9F938E13CD947Ec05AbC7FE734Df8DD826"},"to":{"name":"Bob","wallet":"0xbBbBBBBbbBBBbbbBbbBbbbbBBbBbbbbBbBbbBBbB"},"contents":"Hello, Bob!"}}'
        param.message.version = 'ETH_SIGNTYPEDDATA_V4'

        res = web3_api.createWeb3EthSignTypedData(param)
        txKey = res['txKey']
        print(txKey)
        sig = retrieveSig(web3_api, txKey)['message']['sig']['sig']
        print('sig', sig)

    def test_create_web3_eth_sign_transaction(self):
        config = read_yaml("./config.yaml")
        # EVM
        py_web3 = Web3(Web3.HTTPProvider(config['ethereumRpcApi']))
        # erc20ContractAddress
        token_address = config['erc20ContractAddress']
        # accountTokenAddress
        sender_address = config['accountTokenAddress']
        # toAddress
        recipient_address = config['toAddress']
        # amount
        amount = 1
        # nonce
        nonce = py_web3.eth.get_transaction_count(sender_address)
        # decimals
        decimals = 18
        # amount_in_wei
        amount_in_wei = amount * 10 ** decimals
        transfer_function_signature = 'transfer(address,uint256)'
        data = py_web3.to_hex(py_web3.keccak(text=transfer_function_signature)[:4] +
                              py_web3.to_bytes(hexstr=recipient_address[2:].zfill(64)) +
                              amount_in_wei.to_bytes(32, byteorder='big'))
        gas_limit = py_web3.eth.estimate_gas({
            'to': token_address,
            'from': sender_address,
            'data': data,
        })
        # Get the latest block information
        latest_block = py_web3.eth.get_block('latest')
        # Estimate maxFeePerGas, we assume maxPriorityFeePerGas's value is 2(gwei)
        max_priority_fee_per_gas = py_web3.to_wei(2, "gwei")
        base_fee_per_gas = latest_block['baseFeePerGas']
        # The baseFeePerGas is recommended to be 2 times the latest block's baseFeePerGas value
        # maxFeePerGas must not less than baseFeePerGas + maxPriorityFeePerGas
        max_fee_per_gas = base_fee_per_gas * 2 + max_priority_fee_per_gas

        transaction = {
            'nonce': nonce,
            'to': token_address,
            'data': data,
            'value': 0,
            'chainId': py_web3.eth.chain_id,
            'gas': gas_limit,
            'maxPriorityFeePerGas': max_priority_fee_per_gas,
            'maxFeePerGas': max_fee_per_gas
        }

        web3_api = Web3Api(config)
        param = CreateWeb3EthSignTransactionRequest()
        param.accountKey = config['accountKey']
        param.customerRefId = str(uuid.uuid1())
        param.transaction.to = transaction['to']
        param.transaction.value = transaction['value']
        param.transaction.chainId = transaction['chainId']
        param.transaction.gasLimit = transaction['gas']
        param.transaction.gasPrice = str(py_web3.eth.gas_price)
        param.transaction.nonce = transaction['nonce']
        param.transaction.maxFeePerGas = str(transaction['maxFeePerGas'])
        param.transaction.maxPriorityFeePerGas = str(transaction['maxPriorityFeePerGas'])
        param.transaction.data = data
        res = web3_api.createWeb3EthSignTransaction(param)
        txKey = res['txKey']
        print(txKey)
        sig = retrieveSig(web3_api, txKey)['transaction']['sig']['sig']
        signed_raw_transaction = combine_unsigned_transaction_and_sig(transaction, sig)
        print('signed_raw_transaction', signed_raw_transaction.hex())
        tx_hash = py_web3.eth.send_raw_transaction(signed_raw_transaction.hex()).hex()
        print('tx_hash', tx_hash)
