from safeheron_api_sdk_python.client import *
class GasTransactionsGetByTxKeyRequest:
    def __init__(self):
        # Transaction key, obtained from transactions created via the Create a Transaction V3 API, App, or Web Console.
        self.txKey = None


class GasApi:

    def __init__(self, config):
        self.api_client = Client(config)

    # Retrieve Gas Balance
    # Retrieve your Gas balance for the TRON energy rental service.
    def gas_status(self):
        return self.api_client.send_request(None, '/v1/gas/status')

    # Retrieve Automatic Gas Records for Transactions
    # When the TRON energy rental service is enabled, Safeheron automatically tops up the required Gas fees for TRON network transactions. This API allows you to query the energy rental records used by a transaction. A single transaction may have multiple records. The actual Gas fee consumed by the transaction is the sum of all records with SUCCESS and FAILURE_GAS_CONSUMED statuses.
    def gas_transactions_ge_b_tx_key(self, request: GasTransactionsGetByTxKeyRequest):
        return self.api_client.send_request(request, '/v1/gas/transactions/getByTxKey')
