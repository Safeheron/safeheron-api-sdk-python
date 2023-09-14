import yaml
import sys

sys.path.append('../../../../safeheron_api_sdk_python')
from safeheron_api_sdk_python.api.transaction_api import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestTransaction:

    def test_create_transactions(self):
        config = read_yaml("./config.yaml")
        coin_api = TransactionApi(config)
        param = RecreateTransactionRequest()

        param.coinKey = "ETH_GOERLI"
        param.txAmount = "0.00002"
        param.txFeeLevel = "HIGH"
        param.sourceAccountKey = "account**********46f694ca"
        param.sourceAccountType = "VAULT_ACCOUNT"
        param.destinationAccountType = "ONE_TIME_ADDRESS"
        param.destinationAddress = "0xFA8667a81*************350d35ecaeEF7"
        param.customerRefId = "{{customerRefId}}"

        res = coin_api.create_transactions(param)
        print(res)
