import sys

sys.path.pop(0)
from safeheron_api_sdk_python.client import *


class ListAccountRequest:
    def __init__(self):
        # Page number, start from 1 (default)
        self.pageNumber = None
        # The number of bars per page, the default is 10, max is 100
        self.pageSize = None
        # Filter whether there are not-displayed wallet accounts in Safeheron Console
        # True: retrieve hidden wallet accounts
        # False: retrieve displayed wallet accounts
        # Default: retrieve all wallet accounts
        self.hiddenOnUI = None
        # Filter the response based on this account name prefix
        self.namePrefix = None
        # Filter the response based on this account name suffix
        self.nameSuffix = None


class CreateAccountRequest:
    def __init__(self):
        # Account name, within 30 characters
        self.accountName = None
        # 	Whether display in Safeheron Console
        # True: not display
        # False: display
        # Default: false
        self.hiddenOnUI = None
        # Account tag
        self.accountTag = None
        # Coin key list, 20 array elements max
        self.coinKeyList = None


class BatchCreateAccountRequest:
    def __init__(self):
        # The prefix of wallet account name, 30 characters max
        self.accountName = None
        # Number of wallets to be created, greater than 0, less than 100
        self.count = None
        # Account tag
        self.accountTag = None


class UpdateAccountShowStateRequest:
    def __init__(self):
        # Wallet account key
        self.accountKey = None
        # 	Whether display in Safeheron Console
        # True: not display
        # False: display
        # Default: false
        self.hiddenOnUI = None

class BatchUpdateAccountTagRequest:
    def __init__(self):
        # Wallet account key
        self.accountKey = None
        # Account tag
        self.accountTag = None


class CreateAccountCoinRequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Account key
        self.accountKey = None


class BatchCreateAccountCoinRequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Account key, max is 100
        self.accountKeyList = None
        # Address group name, 30 characters max
        self.addressGroupName = None


class ListAccountCoinRequest:
    def __init__(self):
        # Account key
        self.accountKey = None


class ListAccountCoinAddressRequest:
    def __init__(self):
        # Page number, start from 1 (default)
        self.pageNumber = None
        # The number of bars per page, the default is 10, max is 100
        self.pageSize = None
        # Coin key
        self.coinKey = None
        # Account key
        self.accountKey = None


class InfoAccountCoinAddressRequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Coin receiving address
        self.address = None


class RenameAccountCoinAddressRequest:
    def __init__(self):
        # Address group key
        self.addressGroupKey = None
        # Address group name, 30 characters max
        self.addressGroupName = None


class CreateAccountCoinAddressRequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Account key
        self.accountKey = None
        # Address group name, 30 characters max
        self.addressGroupName = None


class BatchCreateAccountCoinUTXORequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Account key
        self.accountKey = None
        # Address group name, 30 characters max
        self.count = None
        # The number, max is 100
        self.addressGroupName = None


class AccountApi:

    def __init__(self, config):
        global api_client
        api_client = Client(config)

    # List Wallet Accounts
    # Filter wallet account lists in team according to different combinations of conditions.
    def list_accounts(self, request: ListAccountRequest):
        return api_client.send_request(request, '/v1/account/list')

    # Create a new wallet account.
    def create_account(self, request: CreateAccountRequest):
        return api_client.send_request(request, '/v1/account/create')

    # Batch Create Wallet Accounts V1
    # Generate a batch of wallet accounts based on a specified quantity. By default, the wallet accounts created in bulk will not be displayed in the Safeheron App. For optimal results, we recommend using the V2 version.
    def batchCreate_accountV1(self, request: BatchCreateAccountRequest):
        return api_client.send_request(request, '/v1/account/batch/create')

    # Batch Create Wallet Accounts V2
    # Generate a batch of wallet accounts based on a specified quantity. By default, the wallet accounts created in bulk will not be displayed in the Safeheron App.
    def batch_create_accountV2(self, request: BatchCreateAccountRequest):
        return api_client.send_request(request, '/v2/account/batch/create')

    # Change Display of Wallet Account in App
    # Change wallet account status in Safeheron App.
    def update_account_show_state(self, request: UpdateAccountShowStateRequest):
        return api_client.send_request(request, '/v1/account/update/show/state')

    # Batch Label Wallet Accounts
    # Relabel a batch of wallet accounts.
    # Please note that it only supports to label wallets which are created by API. And, the wallets have been used to sweep the target account cannot be relabelled.
    def batch_update_account_tag(self, request: BatchUpdateAccountTagRequest):
        return api_client.send_request(request, '/v1/account/batch/update/tag')

    # Add Coins to a Wallet Account
    # Add a new coin to your wallet account, while generating the default address group for the added coin. Once successfully completed, it will return the address information of the newly created default address group. In case the added currency already exists within the account, it will promptly return the existing default address group information for that coin.
    # In a wallet account, UTXO-based cryptocurrencies can have multiple address groups, while other types of cryptocurrencies usually have only one. To check whether a particular cryptocurrency supports the addition of multiple address groups, simply check the 'isMultipleAddress' parameter through the Coin List.
    def create_account_coin(self, request: CreateAccountCoinRequest):
        return api_client.send_request(request, '/v1/account/coin/create')

    # Batch Add Coins to Wallet Accounts
    # Bulk addition of specified coins to designated wallet accounts. And, it creates a default address group for each coin and returns the address information contained within the newly created default address group. If a wallet account already contains the currency being added, the function will return the default address group data for that existing coin.
    #
    def batch_create_account_coin(self, request: BatchCreateAccountCoinRequest):
        return api_client.send_request(request, '/v1/account/batch/coin/create')

    # List Coins Within a Wallet Account
    # Retrieve a complete list of all coins associated with a wallet account, along with the default address group information for each coin.
    #
    def list_account_coin(self, request: ListAccountCoinRequest):
        return api_client.send_request(request, '/v1/account/coin/list')

    # List Coin Address Group of a Wallet Account
    # Retrieve all address groups for a coin within the wallet account.
    #
    def list_account_coin_address(self, request: ListAccountCoinAddressRequest):
        return api_client.send_request(request, '/v1/account/coin/address/list')

    # Retrieve The Balance of an Address
    # Retrieve the balance of a specific coin address.
    def info_account_coin_address(self, request: InfoAccountCoinAddressRequest):
        return api_client.send_request(request, '/v1/account/coin/address/info')

    # Rename Coin Address Group of a Wallet Account
    # Rename a coin address group of a wallet account.
    def rename_account_coin_address(self, request: RenameAccountCoinAddressRequest):
        return api_client.send_request(request, '/v1/account/coin/address/name')

    # Add Address Group for UTXO-Based Coin
    # Add a new address group for UTXO-based cryptocurrencies under a wallet account. If the coin does not exist, it will be added first, followed by the new address group. The function will return the details of the added address(es).
    def create_account_coin_address(self, request: CreateAccountCoinAddressRequest):
        return api_client.send_request(request, '/v1/account/coin/address/create')

    # Batch Add Address Groups for UTXO-Based Coin
    # For UTXO-based coins in a wallet account, it is possible to add multiple address groups to the account in bulk by specifying the wallet account and the desired number of address groups. The function will return the details of the added address groups. If the specified coin does not exist in the account, it will be added first, followed by the addition of the corresponding number of address groups.
    def batch_create_account_coin_UTXO(self, request: BatchCreateAccountCoinUTXORequest):
        return api_client.send_request(request, '/v1/account/coin/utxo/batch/create')
