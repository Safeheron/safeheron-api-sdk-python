import yaml
import sys

sys.path.append('../../../../safeheron-api-sdk-python')
from safeheron.api.coin_api import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestCoin:

    def test_list_coin(self):
        config = read_yaml("./config.yaml")
        coin_api = CoinApi(config)
        req = coin_api.list_coin()
        print(req)

    def test_check_coin_address(self):
        config = read_yaml("./config.yaml")
        coin_api = CoinApi(config)

        param = CheckCoinAddressRequest()
        param.coinKey = "ETH_GOERLI"
        param.address = "0x75Ab5AB1Eef154C0352Fc31D2428Cef80C7F8B33"
        param.checkContract = True
        param.checkAml = True
        param.checkAddressValid = True

        req = coin_api.check_coin_address(param)
        print(req)
