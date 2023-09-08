import yaml
from safeheron.cosigner.co_signer_converter import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestCoSigner:

    def test_co_signer_converter(self):
        config = read_yaml("./config.yaml")
        converter = CoSignerConverter(config)
        # The CoSignerCallBack received by the controller
        co_signer_call_back = {}
        biz_content = converter.request_convert(co_signer_call_back)
        # According to different types of CoSignerCallBack, the customer handles the corresponding type of business logic.
        print(biz_content)

        coSignerResponse = CoSignerResponse()
        coSignerResponse.approve = True
        coSignerResponse.txKey = "TxKey that needs to be approved"
        encryptResponse = converter.response_converter(coSignerResponse)
        # The customer returns encryptResponse after processing the business logic.
