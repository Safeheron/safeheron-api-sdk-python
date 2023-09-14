import sys

sys.path.pop(0)
from safeheron_api_sdk_python.client import *


class CheckCoinAddressRequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Coin receiving address
        self.address = None
        # Verify contract address (If no value is provided, 'false' by default)
        # True: verify
        # False: not verify
        self.checkContract = None
        # Verify AML compliance (If no value is provided or be verified, AML-compliant address by default)
        # True: verify
        # False: not verify
        self.checkAml = None
        # Verify the validity of address format (If no value is provided, 'false' by dafault)
        # True: verify
        # False: not verify
        self.checkAddressValid = None


class CoinBalanceSnapshotRequest:
    def __init__(self):
        # Only supports querying data within the last 30 days, with the parameter a GMT+8 time in the format of yyyy-MM-dd provided.
        # Note: If the provided value is the current date (not a historical date), it will return the balance up to the current time.
        self.gmt8Date = None


class CoinBlockHeightRequest:
    def __init__(self):
        # Coin key, multiple coin keys are separated by commas
        self.coinKey = None


class CoinApi:

    def __init__(self, config):
        global api_client
        api_client = Client(config)

    # Coin List
    # Retrieve the list of coins supported by Safeheron.
    def list_coin(self):
        return api_client.send_request(None, '/v1/coin/list')

    # Coin Maintenance List
    # Retrieve the information of coins under maintenance in Safeheron.
    def list_coin_maintain(self):
        return api_client.send_request(None, '/v1/coin/maintain/list')

    # Verify Coin Address
    # Verify the correctness of a cryptocurrency address based on the provided validation attributes.
    def check_coin_address(self, request: CheckCoinAddressRequest):
        return api_client.send_request(request, '/v1/coin/address/check')

    # Snapshot the Coin Balance
    # Safeheron takes and stores daily snapshots of balances based on the transaction block's creation time in GMT+8. Please note that the snapshot only keeps data within 30 days.
    def coin_balance_snapshot(self, request: CoinBalanceSnapshotRequest):
        return api_client.send_request(request, '/v1/coin/balance/snapshot')

    # Retrieve Current Block Height for Currency
    # Retrieve the current block height for a specific cryptocurrency by providing its key.
    def coin_block_height(self, request: CoinBlockHeightRequest):
        return api_client.send_request(request, '/v1/coin/block/height')
