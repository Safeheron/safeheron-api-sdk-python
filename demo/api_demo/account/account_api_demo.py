import yaml
import sys

sys.path.append('../../../../safeheron_api_sdk_python')
from safeheron_api_sdk_python.api.account_api import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestAccount:

    def test_list_accounts(self):
        config = read_yaml("./config.yaml")
        account_api = AccountApi(config)
        param = ListAccountRequest()
        param.pageSize = 10
        param.pageNumber = 1
        res = account_api.list_accounts(param)
        print(res)

    def test_create_account(self):
        config = read_yaml("./config.yaml")
        account_api = AccountApi(config)
        param = CreateAccountRequest()
        param.accountName = "accountNameTest"
        res = account_api.create_account(param)
        print(res)
