import sys

sys.path.pop(0)
from safeheron_api_sdk_python.client import *


class CreateWeb3AccountRequest:
    def __init__(self):
        # Account name, within 30 characters
        self.accountName = None
        # 	Whether display in Safeheron Console
        # True: not display
        # False: display
        # Default: false
        self.hiddenOnUI = None


class BatchCreateWeb3AccountRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None


class ListWeb3AccountRequest:
    def __init__(self):
        # Query page direction, NEXT by default
        self.direct = None
        # The number of items to retrieve at a time, default max value is 500
        self.limit = None
        # Txkey of the first transaction record. If the first page has no value, provide the txKey of the last transaction record from the previous result
        self.fromId = None
        # Filter the response based on this account name prefix
        self.namePrefix = None


class CreateWeb3EthSignRequest:
    def __init__(self):
        # Source account key
        self.accountKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Transaction note (180 characters max)
        self.note = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Message Hash
        self.messageHash = self.MessageHash()

    def asDict(self):
        dict = self.__dict__
        dict["messageHash"] = dict["messageHash"].__dict__
        return dict

    class MessageHash:
        def __init__(self):
            # Chain ID (does not participate in signing, only the hash is used for signing)
            self.chainId = None
            # Pending signature hash, hexadecimal string (currently only supports one input)
            self.hash = None


class CreateWeb3PersonalSignRequest:
    def __init__(self):
        # Source account key
        self.accountKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Transaction note (180 characters max)
        self.note = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Message Hash
        self.message = self.Message()

    def asDict(self):
        dict = self.__dict__
        dict["message"] = dict["message"].__dict__
        return dict

    class Message:
        def __init__(self):
            # Chain ID (does not participate in signing, only the hash is used for signing)
            self.chainId = None
            # Data to be signed
            self.data = None


class CreateWeb3EthSignTypedDataRequest:
    def __init__(self):
        # Source account key
        self.accountKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Transaction note (180 characters max)
        self.note = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Message Hash
        self.message = self.Message()

    def asDict(self):
        dict = self.__dict__
        dict["message"] = dict["message"].__dict__
        return dict

    class Message:
        def __init__(self):
            # Chain ID (does not participate in signing, only the hash is used for signing)
            self.chainId = None
            # Data to be signed
            self.data = None
            # EthSignTypedData Version
            self.version = None


class CreateWeb3EthSignTransactionRequest:
    def __init__(self):
        # Source account key
        self.accountKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Transaction note (180 characters max)
        self.note = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Transaction
        self.transaction = self.Transaction()

    def asDict(self):
        dict = self.__dict__
        dict["transaction"] = dict["transaction"].__dict__
        return dict

    class Transaction:
        def __init__(self):
            # To
            self.to = None
            # Value (Unit: wei)
            self.value = None
            # Chain ID
            self.chainId = None
            # Gas price
            self.gasPrice = None
            # Gas limit
            self.gasLimit = None
            # Max priority fee per gas for EIP-1559
            self.maxPriorityFeePerGas = None
            # Max fee per gas for EIP-1559
            self.maxFeePerGas = None
            # Nonce
            self.nonce = None
            # Data
            self.data = None


class CancelWeb3SignRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None


class OneWeb3SignRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None


class ListWeb3SignRequest:
    def __init__(self):
        # Query page direction, NEXT by default
        self.direct = None
        # The number of items to retrieve at a time, default max value is 500
        self.limit = None
        # Txkey of the first transaction record. If the first page has no value, provide the txKey of the last transaction record from the previous result
        self.fromId = None
        # Web3 Sign type
        self.subjectType = None
        # Transaction status
        self.transactionStatus = None
        # Source account key
        self.accountKey = None
        # Start time for creating a transaction, UNIX timestamp (ms) (If no value is provided, the default value is createTimeMax minus 24 hours)
        self.createTimeMin = None
        # End time for creating a transaction, UNIX timestamp (ms) (If no value is provided, the default value is the current UTC time)
        self.createTimeMax = None


class Web3Api:

    def __init__(self, config):
        global api_client
        api_client = Client(config)

    # Create a Web3 Wallet Account
    def createWeb3Account(self, request: CreateWeb3AccountRequest):
        return api_client.send_request(request, '/v1/web3/account/create')

    # Batch Create Web3 Wallet Accounts
    # Create a batch of wallet accounts based on specified number. Web3 wallet accounts created in batches are not displayed in the Safeheron App by default.
    def batchCreateWeb3Account(self, request: BatchCreateWeb3AccountRequest):
        return api_client.send_request(request, '/v1/web3/batch/account/create')

    # List Web3 Wallet Accounts
    # Filter Web3 wallet account lists by various conditions.
    def listWeb3Accounts(self, request: ListWeb3AccountRequest):
        return api_client.send_request(request, '/v1/web3/account/list')

    # Create ethSign
    # Merchants can initiate an ethSign signature through this interface. The merchant is required to serialize the transaction data, generating a corresponding hash (supporting both 0x and non-0x formatted data). The hash is then submitted through this interface to create a signature, which can be obtained by Retrieve a Single Web3 Signature interface or webhook. From there, merchants can complete the subsequent steps according to their own needs once they have obtained the signature.
    def createWeb3EthSign(self, request: CreateWeb3EthSignRequest):
        request.asDict();
        return api_client.send_request(request, '/v1/web3/sign/ethSign')

    # Create personalSign
    # Merchants can initiate a personalSign signature for any text using this interface. The merchant only needs to prepare the data to be signed and submit it through this interface to create the signature. The resulting signature can then be obtained by Retrieve a Single Web3 Signature interface or via webhook. From there, merchants can complete the subsequent steps according to their own needs once they have obtained the signature.
    def createWeb3PersonalSign(self, request: CreateWeb3PersonalSignRequest):
        request.asDict()
        return api_client.send_request(request, '/v1/web3/sign/personalSign')

    # Create ethSignTypedData
    # Merchants can initiate an ethSignTypedData signature of specific formatted data (supporting data formats of v1, v3, and v4) through this interface. Merchants will need to format their signature data and submit it through the interface. Once the signature is created, the result can be retrieved via Retrieve a Single Web3 Signature interface or webhook. From there, merchants can complete the subsequent steps according to their own needs once they have obtained the signature.
    def createWeb3EthSignTypedData(self, request: CreateWeb3EthSignTypedDataRequest):
        request.asDict()
        return api_client.send_request(request, '/v1/web3/sign/ethSignTypedData')

    # Create ethSignTransaction
    # Merchants can initiate ethSignTransaction signature transactions through this interface. The merchant must prepare transaction-related data, such as from, to, nonce, gas limit, gas price, value, data, and more. Once this data is submitted, a signature is created and the result can be obtained by Retrieve a Single Web3 Signature interface or webhook. From there, merchants can complete the subsequent steps according to their own needs once they have obtained the signature.
    def createWeb3EthSignTransaction(self, request: CreateWeb3EthSignTransactionRequest):
        request.asDict()
        return api_client.send_request(request, '/v1/web3/sign/ethSignTransaction')

    # Cancel Signature
    # Cancel pending signatures.
    def cancelWeb3Sign(self, request: CancelWeb3SignRequest):
        return api_client.send_request(request, '/v1/web3/sign/cancel')

    # Retrieve a Single Web3 Signature
    # To query a transaction, either customerRefId or txKey are required. If both values are provided, the retrieval will be based on the txKey.
    def oneWeb3Sign(self, request: OneWeb3SignRequest):
        return api_client.send_request(request, '/v1/web3/sign/one')

    # Web3 Sign Transaction List
    # Filter Web3 Sign history by various conditions.
    def listWeb3Sign(self, request: ListWeb3SignRequest):
        return api_client.send_request(request, '/v1/web3/sign/list')
