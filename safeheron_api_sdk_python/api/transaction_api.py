import sys

sys.path.pop(0)
from safeheron_api_sdk_python.client import *


class ListTransactionsV1Request:
    def __init__(self):
        # Page number, start from 1 (default)
        self.pageNumber = None
        # The number of bars per page, the default is 10, max is 100
        self.pageSize = None
        # Source account key
        self.sourceAccountKey = None
        # Source account type
        self.sourceAccountType = None
        # Destination account key
        self.destinationAccountKey = None
        # Destination account type
        self.destinationAccountType = None
        # Start time for creating a transaction, UNIX timestamp (ms)
        self.createTimeMin = None
        # End time for creating a transaction, UNIX timestamp (ms)
        self.createTimeMax = None
        # Min transaction amount
        self.txAmountMin = None
        # Max transaction amount
        self.txAmountMax = None
        # Coin key, multiple coin keys are separated by commas
        self.coinKey = None
        # Transaction fee coin key, multiple coin keys are separated by commas
        self.feeCoinKey = None
        # Transaction status
        self.transactionStatus = None
        # Transaction substatus
        self.transactionSubStatus = None
        # Min duration for completing a transaction, UNIX timestamp (ms)
        self.completedTimeMin = None
        # Max duration for completing a transaction, UNIX timestamp (ms)
        self.completedTimeMax = None
        # Merchant unique business ID
        self.customerRefId = None
        # Type of actual destination account
        self.realDestinationAccountType = None
        # Filter out custom transaction amounts, excluding transaction records below a certain amount specified in USD from the query results
        self.hideSmallAmountUsd = None


class ListTransactionsV2Request:
    def __init__(self):
        # Query page direction, NEXT by default
        self.direct = None
        # The number of items to retrieve at a time, default max value is 500
        self.limit = None
        # Txkey of the first transaction record. If the first page has no value, provide the txKey of the last transaction record from the previous result
        self.fromId = None
        # Source account key
        self.sourceAccountKey = None
        # Source account type
        self.sourceAccountType = None
        # Destination account key
        self.destinationAccountKey = None
        # Destination account type
        self.destinationAccountType = None
        # Start time for creating a transaction, UNIX timestamp (ms)
        self.createTimeMin = None
        # End time for creating a transaction, UNIX timestamp (ms)
        self.createTimeMax = None
        # Min transaction amount
        self.txAmountMin = None
        # Max transaction amount
        self.txAmountMax = None
        # Coin key, multiple coin keys are separated by commas
        self.coinKey = None
        # Transaction fee coin key, multiple coin keys are separated by commas
        self.feeCoinKey = None
        # Transaction status
        self.transactionStatus = None
        # Transaction substatus
        self.transactionSubStatus = None
        # Min duration for completing a transaction, UNIX timestamp (ms)
        self.completedTimeMin = None
        # Max duration for completing a transaction, UNIX timestamp (ms)
        self.completedTimeMax = None
        # Merchant unique business ID
        self.customerRefId = None
        # Type of actual destination account
        self.realDestinationAccountType = None
        # Filter out custom transaction amounts, excluding transaction records below a certain amount specified in USD from the query results
        self.hideSmallAmountUsd = None


class CreateTransactionRequest:
    def __init__(self):
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Transaction note (180 characters max)
        self.note = None
        # Coin key
        self.coinKey = None
        # Transaction Fee Rate Grade
        # Choose between transaction fees. If the transaction fee rate is preset, it will take priority
        self.txFeeLevel = None
        # Transaction fee rate, either txFeeLevel or feeRateDto
        self.feeRateDto = FeeRateDto()
        # Maximum estimated transaction fee rate for a given transaction
        self.maxTxFeeRate = None
        # Transaction amount
        self.txAmount = None
        # Deduct transaction fee from the transfer amount
        # False by default. If set to true, transaction fee will be deducted from the transfer amount
        # Note: This parameter can only be considered if a transaction’s asset is a base asset, such as ETH or MATIC. If the asset can’t be used for transaction fees, like USDC, this parameter is ignored
        self.treatAsGrossAmount = None
        # Source account key
        self.sourceAccountKey = None
        # Account type
        self.sourceAccountType = None
        # Destination account key
        # Whitelist key if the destination is a whitelisted account;
        # Wallet account key if the destination is a wallet account;
        # No key for unknown address
        self.destinationAccountKey = None
        # Destination account type
        self.destinationAccountType = None
        # If the destinationAccountType is ONE_TIME_ADDRESS, then this field should have a value
        self.destinationAddress = None
        # Destination Tag
        self.destinationTag = None
        # Bitcoin enabled for RBF (Replace-by-fee is a protocol in the Bitcoin mempool that allows for the replacement of an unconfirmed transaction with another one)
        self.isRbf = None
        # The default setting for the parameter is [true]. This parameter determines whether a transaction can be created when the target address is a smart contract. If set to [false], a transaction can still be created for a contract address
        self.failOnContract = None
        # Custom nonce
        self.nonce = None
        # Balance verification, BALANCE_CHECK by default
        self.balanceVerifyType = None

    def asDict(self):
        dict = self.__dict__
        dict["feeRateDto"] = dict["feeRateDto"].__dict__
        return dict


class FeeRateDto:
    def __init__(self):
        # Fee rate: fee per byte for UTXO, gas price for EVM chains, free limit for TRON (optional) and gas price for SUI
        self.feeRate = None
        # EVM gas limit
        self.gasLimit = None
        # EIP-1559 max priority fee
        self.maxPriorityFee = None
        # EIP-1559 max fee
        self.maxFee = None
        # Filecoin gas premium, similar to EIP-1559 max priority fee
        self.gasPremium = None
        # Filecoin gas fee cap, similar to EIP-1559 max fee
        self.gasFeeCap = None
        # SUI gas budget, similar to EIP-1559 max fee
        self.gasBudget = None


class RecreateTransactionRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None
        # Transaction hash
        self.txHash = None
        # Coin key
        self.coinKey = None
        # Transaction Fee Rate Grade
        # Choose between transaction fees. If the transaction fee rate is preset, it will take priority
        self.txFeeLevel = None
        # Transaction fee rate, either txFeeLevel or feeRateDto
        self.feeRateDto = FeeRateDto()

    def asDict(self):
        dict = self.__dict__
        dict["feeRateDto"] = dict["feeRateDto"].__dict__
        return dict


class OneTransactionsRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None


class TransactionsFeeRateRequest:
    def __init__(self):
        # Coin key
        self.coinKey = None
        # Transaction hash, pass the original transaction hash when speed up transaction estimation
        self.txHash = None
        # Source account key, required for UTXO-based coins
        self.sourceAccountKey = None
        # Source address are required for TRON when estimating transaction fees. For EVM-based transactions, the source address is required when retrieving the gas limit on the blockchain. Otherwise, a default fixed gas limit value will be returned
        self.sourceAddress = None
        # Destination address is optional for TRON and FIL when estimating transaction fees (although providing it may result in a more accurate fee estimation). For EVM-based transactions, the destination address is required when retrieving the gas limit on the blockchain. Otherwise, a default fixed gas limit value will be returned
        self.destinationAddress = None
        # Transfer amount is required to calculate gas limit more accurately when using EVM chains. When using UTXO, providing the amount can estimate transaction fees more accurately. If no amount is provided, the calculation is based on the maximum UTXO quantity. When using SUI, providing the amount can estimate gas budget more accurately
        self.value = None


class CancelTransactionRequest:
    def __init__(self):
        # Transaction key
        self.txKey = None
        # Transaction type, TRANSACTION by default
        self.txType = None


class CollectionTransactionsUTXORequest:
    def __init__(self):
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt1 = None
        # Merchant extended field (defined by merchant) shown to merchant (255 characters max)
        self.customerExt2 = None
        # Transaction note (180 characters max)
        self.note = None
        # Coin key
        self.coinKey = None
        # Transaction fee rate, the unit is the feeUnit returned by the coin list
        self.txFeeRate = None
        # Transaction Fee Rate Grade
        # Choose between the transaction fee rate. If the transaction fee rate is preset, it will take priority
        self.txFeeLevel = None
        # Maximum estimated transaction fee rate for a given transaction
        self.maxTxFeeRate = None
        # Minimum sweeping amount
        self.minCollectionAmount = None
        # Source account key
        self.sourceAccountKey = None
        # Account type
        self.sourceAccountType = None
        # Destination account key
        self.destinationAccountKey = None
        # Destination account type
        self.destinationAccountType = None
        # If the destinationAccountType is ONE_TIME_ADDRESS, then this field should have a value
        self.destinationAddress = None
        # Destination Tag
        self.destinationTag = None


class TransactionApi:

    def __init__(self, config):
        global api_client
        api_client = Client(config)

    # Transaction List V1
    # Filter transaction history by various conditions. For optimal results, we recommend using the V2 version.
    def list_transactions_v1(self, request: ListTransactionsV1Request):
        return api_client.send_request(request, '/v1/transactions/list')

    # Transaction List V2
    # Filter transaction history by various conditions.
    def list_transactions_v2(self, request: ListTransactionsV2Request):
        return api_client.send_request(request, '/v2/transactions/list')

    # Create a new transaction.
    def create_transactions(self, request: CreateTransactionRequest):
        request.asDict()
        return api_client.send_request(request, '/v2/transactions/create')

    # Speed up EVM and UTXO-based Transactions
    # Transactions with low transaction fees and those that have been pending for a long time can be sped up. EVM-based and BTC transactions can be sped up through RBF(If 'isRbf' is set to true during transaction creation, the transaction will be accelerated using RBF acceleration. Otherwise, CPFP acceleration will be used.) For other UTXO-based transactions, CPFP will be used.
    def recreate_transactions(self, request: RecreateTransactionRequest):
        request.asDict()
        return api_client.send_request(request, '/v2/transactions/recreate')

    # Retrieve a Transaction
    # To query a transaction, either customerRefId or txKey are required. If both values are provided, the retrieval will be based on the txKey.
    def one_transactions(self, request: OneTransactionsRequest):
        return api_client.send_request(request, '/v1/transactions/one')

    # Estimate Transaction Fee
    # This interface provides users with an estimated range of transaction fee rates of a given cryptocurrency when creating or speeding up transactions.
    def transaction_fee_rate(self, request: TransactionsFeeRateRequest):
        return api_client.send_request(request, '/v2/transactions/getFeeRate')

    # Cancel Transaction
    # Cancel the authorization-pending transaction and the signing-in-progress transaction.
    def cancel_transactions(self, request: CancelTransactionRequest):
        return api_client.send_request(request, '/v1/transactions/cancel')

    # UTXO-Based Coin Sweeping
    # For multi-address UTXO coins under a wallet account, this interface allows users to collect the balances of certain qualifying addresses into a specified destination address.
    def collectionTransactionsUTXO(self, request: CollectionTransactionsUTXORequest):
        return api_client.send_request(request, '/v1/transactions/utxo/collection')
