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
        # Filter transaction history by transaction direction:
        # Default: Retrieve all types of transactions
        # INFLOW: Retrieve inflows
        # OUTFLOW: Retrieve outflows
        # INTERNAL_TRANSFER: Retrieve internal transfers
        self.transactionDirection = None


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
        # Filter transaction history by transaction direction:
        # Default: Retrieve all types of transactions
        # INFLOW: Retrieve inflows
        # OUTFLOW: Retrieve outflows
        # INTERNAL_TRANSFER: Retrieve internal transfers
        self.transactionDirection = None


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
        # The memo (up to 100 characters) for the destination address, also known as a comment or tag. This parameter is valid for transactions on the following networks:
        # TON: TON mainnet
        # TON_TESTNET: TON testnet
        self.memo = None
        # Destination Tag
        self.destinationTag = None
        # Bitcoin enabled for RBF (Replace-by-fee is a protocol in the Bitcoin mempool that allows for the replacement of an unconfirmed transaction with another one)
        self.isRbf = None
        # The default setting for the parameter is [true]. This parameter determines whether a transaction can be created when the target address is a smart contract. If set to [false], a transaction can still be created for a contract address
        self.failOnContract = None
        # Default value is true. When initiating and approving transactions, Safeheron assesses the destinationAddress for risk through its AML/KYT service provider. It then decides whether to permit the transaction based on this assessment. By default, if the destination address presents compliance risks, the system prohibits the transaction.
        # If you fully understand the associated risks and still need to transfer funds to this address, you can explicitly set failOnAml to false. In this case, Safeheron will disregard the risk assessment results and allow the transaction to proceed.
        self.failOnAml = None
        # Custom nonce
        self.nonce = None
        # Customizable sequence number on Aptos, similar to the nonce in the EVM.
        self.sequenceNumber = None
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
        # The gas price the transaction sender is willing to pay, similar to EVM gasPrice
        self.gasUnitPrice = None
        # The maximum number of gas units that the transaction sender is willing to spend to execute the transaction, similar to EVM gasLimit
        self.maxGasAmount = None

class CreateTransactionsUTXOMultiDestRequest:
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
        # Source account key
        self.sourceAccountKey = None
        # Account type
        self.sourceAccountType = None
        # Destination address list
        self.destinationAddressList = [DestinationAddress]
        # Destination Tag
        self.destinationTag = None
        # Bitcoin enabled for RBF (Replace-by-fee is a protocol in the Bitcoin mempool that allows for the replacement of an unconfirmed transaction with another one)
        self.isRbf = None
        # Default value is true. When initiating and approving transactions, Safeheron assesses the destinationAddress for risk through its AML/KYT service provider. It then decides whether to permit the transaction based on this assessment. By default, if the destination address presents compliance risks, the system prohibits the transaction.
        # If you fully understand the associated risks and still need to transfer funds to this address, you can explicitly set failOnAml to false. In this case, Safeheron will disregard the risk assessment results and allow the transaction to proceed.
        self.failOnAml = None

    def asDict(self):
        dict = self.__dict__
        dict["feeRateDto"] = dict["feeRateDto"].__dict__
        destinationAddressList = []
        for item in dict["destinationAddressList"]:
            destinationAddressList.append(item.__dict__)
        dict["destinationAddressList"] = destinationAddressList
        return dict

class DestinationAddress:
    def __init__(self):
        # Destination address
        self.address = None
        # Transaction amount
        self.amount = None


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

class ApprovalDetailTransactionsRequest:
    def __init__(self):
        # Transaction key list within 20 transaction keys
        self.txKeyList = None


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
        # Destination address list
        self.destinationAddressList = [DestinationAddress]
        # Transfer amount is required to calculate gas limit more accurately when using EVM chains. When using UTXO, providing the amount can estimate transaction fees more accurately. If no amount is provided, the calculation is based on the maximum UTXO quantity. When using SUI, providing the amount can estimate gas budget more accurately
        self.value = None

    def asDict(self):
        dict = self.__dict__
        destinationAddressList = []
        for item in dict["destinationAddressList"]:
            destinationAddressList.append(item.__dict__)
        dict["destinationAddressList"] = destinationAddressList
        return dict


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
        self.api_client = Client(config)

    # Transaction List V1
    # Filter transaction history by various conditions. For optimal results, we recommend using the V2 version.
    def list_transactions_v1(self, request: ListTransactionsV1Request):
        return self.api_client.send_request(request, '/v1/transactions/list')

    # Transaction List V2
    # Filter transaction history by various conditions.
    def list_transactions_v2(self, request: ListTransactionsV2Request):
        return self.api_client.send_request(request, '/v2/transactions/list')

    # Create a new transaction.
    def create_transactions(self, request: CreateTransactionRequest):
        request.asDict()
        return self.api_client.send_request(request, '/v2/transactions/create')

    # Create a new transaction.
    
    def create_transactions_v3(self, request: CreateTransactionRequest):
        request.asDict()
        return self.api_client.send_request(request, '/v3/transactions/create')

    # For UTXOs that natively support multiple OUTPUTs, this interface allows a single transaction to transfer funds to multiple destination addresses simultaneously.(To use the Co-Signer, please use version 1.5.9 or higher)
    def create_transactions_UTXO_multiDest(self, request: CreateTransactionsUTXOMultiDestRequest):
        request.asDict()
        return self.api_client.send_request(request, '/v1/transactions/utxo/multidest/create')

    # Speed up EVM and UTXO-based Transactions
    # Transactions with low transaction fees and those that have been pending for a long time can be sped up. EVM-based and BTC transactions can be sped up through RBF(If 'isRbf' is set to true during transaction creation, the transaction will be accelerated using RBF acceleration. Otherwise, CPFP acceleration will be used.) For other UTXO-based transactions, CPFP will be used.
    def recreate_transactions(self, request: RecreateTransactionRequest):
        request.asDict()
        return self.api_client.send_request(request, '/v2/transactions/recreate')

    # Retrieve a Transaction
    # To query a transaction, either customerRefId or txKey are required. If both values are provided, the retrieval will be based on the txKey.
    def one_transactions(self, request: OneTransactionsRequest):
        return self.api_client.send_request(request, '/v1/transactions/one')

    # Retrieve Transaction Approval Details
    # Query approval details of a transaction. Exclusively for transactions using the new advanced transaction policy. Learn more about new advanced transaction policies.
    def approval_detail_transactions(self, request: ApprovalDetailTransactionsRequest):
        return self.api_client.send_request(request, '/v1/transactions/approvalDetail')

    # Estimate Transaction Fee
    # This interface provides users with an estimated range of transaction fee rates of a given cryptocurrency when creating or speeding up transactions.
    def transaction_fee_rate(self, request: TransactionsFeeRateRequest):
        return self.api_client.send_request(request, '/v2/transactions/getFeeRate')

    # Cancel Transaction
    # Cancel the authorization-pending transaction and the signing-in-progress transaction.
    def cancel_transactions(self, request: CancelTransactionRequest):
        return self.api_client.send_request(request, '/v1/transactions/cancel')

    # UTXO-Based Coin Sweeping
    # For multi-address UTXO coins under a wallet account, this interface allows users to collect the balances of certain qualifying addresses into a specified destination address.
    def collectionTransactionsUTXO(self, request: CollectionTransactionsUTXORequest):
        return self.api_client.send_request(request, '/v1/transactions/utxo/collection')
