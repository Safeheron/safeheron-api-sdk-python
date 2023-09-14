import sys

sys.path.pop(0)
from safeheron_api_sdk_python.client import *


class CreateMPCSignTransactionRequest:
    def __init__(self):
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Source account key
        self.sourceAccountKey = None
        # Signature algorithm
        self.signAlg = None
        # Transaction fee rate, either txFeeLevel or feeRateDto
        self.dataList = [self.Date()]

    def asDict(self):
        dict = self.__dict__
        dict["dataList"] = [data.__dict__ for data in dict["dataList"]]
        return dict

    class Date:
        def __init__(self):
            # Transaction note (180 characters max)
            self.note = None
            # Transaction data to be signed (view description below for details)
            self.data = None


class OneMPCSignTransactionsRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None


class ListMPCSignTransactionsRequest:
    def __init__(self):
        # Query page direction, NEXT by default
        self.direct = None
        # The number of items to retrieve at a time, default max value is 500
        self.limit = None
        # Txkey of the first transaction record. If the first page has no value, provide the txKey of the last transaction record from the previous result
        self.fromId = None
        # Start time for creating a transaction, UNIX timestamp (ms) (If no value is provided, the default value is createTimeMax minus 24 hours)
        self.createTimeMin = None
        # End time for creating a transaction, UNIX timestamp (ms) (If no value is provided, the default value is the current UTC time)
        self.createTimeMax = None


class MPCSignApi:

    def __init__(self, config):
        global api_client
        api_client = Client(config)

    # Create an MPC Sign Transaction
    # Merchant can initiate MPC Sign via this interface. The merchant must first serialize the transaction data and generate a hash before using this interface to submit the hash and create a transaction. The resulting signature can be retrieved via the MPC Sign transaction interface or webhook. The merchant can proceed with the necessary follow-up processes to obtain the signature according to their specific needs.
    def create_mpc_sign_transactions(self, request: CreateMPCSignTransactionRequest):
        request.asDict()
        return api_client.send_request(request, '/v1/transactions/mpcsign/create')

    # Retrieve a Single MPC Sign Transaction
    # To query a specific MPC Sign transaction, either customerRefId or txKey must be provided. If both parameters are provided, the query will be based on the txKey parameter.
    def one_mpc_sign_transactions(self, request: OneMPCSignTransactionsRequest):
        return api_client.send_request(request, '/v1/transactions/mpcsign/one')

    # MPC Sign Transaction List
    # Filter MPC Sign transaction history by various conditions.
    def list_mpc_sign_transactions(self, request: ListMPCSignTransactionsRequest):
        return api_client.send_request(request, '/v1/transactions/mpcsign/list')
