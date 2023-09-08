import json

import yaml
from safeheron.api.mpc_sign_api import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestMPCSign:
    def test_create_MPC_sign_transactions(self):
        config = read_yaml("./config.yaml")
        coin_api = MPCSignApi(config)
        param = CreateMPCSignTransactionRequest()

        param.signAlg = "ed25519"
        param.sourceAccountKey = "account08a23**********99dc6346f694ca"
        param.dataList[0].data = "d061e9c5891*********714cc7e7a9215f0071ef5a5723f69"
        param.customerRefId = "{{customerRefId}}"
        res = coin_api.create_MPC_sign_transactions(param)
        print(res)
