import yaml
import sys
from web3 import Web3

sys.path.append('../../../../safeheron_api_sdk_python')
from safeheron_api_sdk_python.api.mpc_sign_api import *

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


def retrieveSig(mpc_sign_api, tx_key):
    i = 1
    while i <= 100:
        i += 1
        queryParam = OneMPCSignTransactionsRequest()
        queryParam.txKey = tx_key
        one = mpc_sign_api.one_mpc_sign_transactions(queryParam)
        print('sign status:', one['transactionStatus'])
        if one['transactionStatus'] == 'COMPLETED':
            return one
        time.sleep(5)


class TestMPCSign:
    def test_create_MPC_sign_transactions(self):
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

        mpc_sign_api = MPCSignApi(config)
        param = CreateMPCSignTransactionRequest()
        param.signAlg = 'Secp256k1'
        param.sourceAccountKey = config['accountKey']
        param.customerRefId = str(uuid.uuid1())
        param.dataList[0].data = transaction_hash.hex()

        res = mpc_sign_api.create_mpc_sign_transactions(param)
        print(res)
        txKey = res['txKey']
        print(txKey)
        sig = retrieveSig(mpc_sign_api, txKey)['dataList'][0]['sig']
        signed_raw_transaction = combine_unsigned_transaction_and_sig(transaction, sig)
        print('signed_raw_transaction', signed_raw_transaction.hex())
        tx_hash = py_web3.eth.send_raw_transaction(signed_raw_transaction.hex()).hex()
        print('tx_hash', tx_hash)
