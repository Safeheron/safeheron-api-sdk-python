from safeheron_api_sdk_python.client import *


class ListWhitelistRequest:
    def __init__(self):
        # Query page direction, NEXT by default
        self.direct = None
        # The number of items to retrieve at a time, default max value is 500
        self.limit = None
        # Txkey of the first transaction record. If the first page has no value, provide the txKey of the last transaction record from the previous result
        self.fromId = None
        # The supported public blockchains for whitelist addresses are:
        # EVM: Ethereum-compatible public chain networks or Layer 2 addresses that can receive its native token and other tokens
        # Bitcoin: Bitcoin mainnet addresses that can receive Bitcoin
        # Bitcoin Cash: Bitcoin Cash network, which can receive BCH
        # Dash: anonymous Dash network, which can receive DASH
        # TRON: Tron mainnet addresses, which can receive TRX and TRC20 tokens, such as USDT and USDC
        # NEAR: NEAR mainnet, which can receive native token NEAR
        # Filecoin: Receive Filecoin native token FIL, but does not support receiving FIL or tokens from the FVM network
        # Sui: Sui mainnet, which can receive native token Sui and other tokens
        # Aptos: Aptos mainnet, which only supports receiving native token Aptos and does not support other tokens yet
        # Solana: Solana mainnet, which can receive native token SOL and other tokens
        # Bitcoin Testnet: Bitcoin testnet, which can receive Bitcoin testnet ass
        self.chainType = None
        # Whitelist status
        # AUDIT: pending approval
        # APPROVED: active
        # REJECTED: rejected
        self.whitelistStatus = None
        # Start time for creating a whitelist in UNIX timestamp (ms) (If no value is provided, the default value is createTimeMax minus 24 hours)
        self.createTimeMin = None
        # End time for creating a whitelist in UNIX timestamp (ms) (If no value is provided, the default value is the current UTC time)
        self.createTimeMax = None


class OneWhitelistRequest:
    def __init__(self):
        # Whitelist unique identifier. It is required if address is not provided. If both are provided, the whitelistKey takes precedence
        self.whitelistKey = None
        # Whitelist address. It is required if whitelistKey is not provided and please make sure the provided address is correct
        self.address = None


class CreateWhitelistRequest:
    def __init__(self):
        # Whitelist unique name, 20 characters max
        self.whitelistName = None
        # The supported public blockchains for whitelist addresses are:
        # EVM: Ethereum-compatible public chain networks or Layer 2 addresses that can receive its native token and other tokens
        # Bitcoin: Bitcoin mainnet addresses that can receive Bitcoin
        # Bitcoin Cash: Bitcoin Cash network, which can receive BCH
        # Dash: anonymous Dash network, which can receive DASH
        # TRON: Tron mainnet addresses, which can receive TRX and TRC20 tokens, such as USDT and USDC
        # NEAR: NEAR mainnet, which can receive native token NEAR
        # Filecoin: Receive Filecoin native token FIL, but does not support receiving FIL or tokens from the FVM network
        # Sui: Sui mainnet, which can receive native token Sui and other tokens
        # Aptos: Aptos mainnet, which only supports receiving native token Aptos and does not support other tokens yet
        # Solana: Solana mainnet, which can receive native token SOL and other tokens
        # Bitcoin Testnet: Bitcoin testnet, which can receive Bitcoin testnet assets
        self.chainType = None
        # Public blockchain address and the address format needs to meet the requirements of the chain
        self.address = None
        #  The memo (up to 20 characters) for the destination address, also known as a comment or tag. For the following networks, if a destination address memo was set initially, a memo matching the one in the transaction record must be provided
        #  TON: TON mainnet
        #  TON_TESTNET: TON testnet
        self.memo = None
        # Visibility status in Safeheron App and Web Console
        # False: Visible by default
        # True: Invisible; the invisible whitelist can only be managed and used through the API, such as querying, modifying, and using the whitelist as the destination address when initiating transactions
        self.hiddenOnUI = None


class CreateFromTransactionWhitelistRequest:
    def __init__(self):
        # Whitelist unique name, 20 characters max
        self.whitelistName = None
        # Transaction key
        self.txKey = None
        # The destination address in the transaction record; case-sensitive
        self.destinationAddress = None
        #  The memo (up to 20 characters) for the destination address, also known as a comment or tag. For the following networks, if a destination address memo was set initially, a memo matching the one in the transaction record must be provided
        #  TON: TON mainnet
        #  TON_TESTNET: TON testnet
        self.memo = None
        # Visibility status in Safeheron App and Web Console
        # False: Visible by default
        # True: Invisible; the invisible whitelist can only be managed and used through the API, such as querying, modifying, and using the whitelist as the destination address when initiating transactions
        self.hiddenOnUI = None


class EditWhitelistRequest:
    def __init__(self):
        # Whitelist unique identifier
        self.whitelistKey = None
        # Whitelist unique name, 20 characters max
        self.whitelistName = None
        # Public blockchain address and the address format needs to meet the requirements of the chain
        self.address = None
        #  The memo (up to 20 characters) for the destination address, also known as a comment or tag. For the following networks, if a destination address memo was set initially, a memo matching the one in the transaction record must be provided
        #  TON: TON mainnet
        #  TON_TESTNET: TON testnet
        self.memo = None
        # When the whitelist is involved in a transaction approval policy, modifications will result in the new whitelist being directly applied to the approval policy. False by default, meaning that when involved in a transaction approval policy, it will not be modified.
        self.force = None


class DeleteWhitelistRequest:
    def __init__(self):
        # Whitelist unique identifier
        self.whitelistKey = None


class WhitelistApi:

    def __init__(self, config):
        self.api_client = Client(config)

    # List Whitelist Data
    # Paginate the whitelist data based on the query criteria.
    def list_whitelist(self, request: ListWhitelistRequest):
        return self.api_client.send_request(request, '/v1/whitelist/list')

    # Retrieve a Single Whitelist
    #      * Retrieve the data of a whitelist.
    def one_whitelist(self, request: OneWhitelistRequest):
        return self.api_client.send_request(request, '/v1/whitelist/one')

    # Create a Whitelist
    # Add a new whitelisted address. The newly added address needs to be approved in the Safeheron App before it becomes effective. The approval details are as follows:
    # Admin approval: If a custom whitelist approval process is not set, it will become effective after being approved by the team admins according to the team's decision-making process.
    # Custom whitelist approval: If a whitelist approval process is set, it will become effective after being approved according to the process.
    def create_whitelist(self, request: CreateWhitelistRequest):
        return self.api_client.send_request(request, '/v1/whitelist/create')

    # Create a Whitelist Based on a Transaction
    # Whitelist the transaction's destination address when the transaction meets the following conditions:
    #
    # A transfer transaction from an asset wallet; Web3 wallet transactions or MPC Sign transactions are not supported.
    # The transaction is in a completed state as COMPLETED.
    # The transaction's destination address is a one-time address.
    def create_from_transaction_whitelist(self, request: CreateFromTransactionWhitelistRequest):
        return self.api_client.send_request(request, '/v1/whitelist/createFromTransaction')

    # Modify a Whitelist
    # Modify a whitelist based on its unique identifier. The whitelist only supports modifying its name and address; whitelists pending for approval cannot be modified. After modifying the whitelist, it needs to be reviewed and approved in the Safeheron App before it becomes effective. The approval details are as follows:
    # Admin approval: If a custom whitelist approval process is not set, it will become effective after being approved by the team admins according to the team's decision-making process.
    # Custom whitelist approval: If a whitelist approval process is set, it will become effective after being approved according to the process.
    def edit_whitelist(self, request: EditWhitelistRequest):
        return self.api_client.send_request(request, '/v1/whitelist/edit')

    # Delete a Whitelist
    # To delete a whitelisted address, note that no approval is required for deletion. If a whitelisted address that is under approval is deleted, the approval task will also be automatically cancelled.
    def delete_whitelist(self, request: DeleteWhitelistRequest):
        return self.api_client.send_request(request, '/v1/whitelist/delete')
