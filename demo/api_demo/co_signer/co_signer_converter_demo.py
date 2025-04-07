import yaml
import sys

sys.path.append('../../../../safeheron_api_sdk_python')
from safeheron_api_sdk_python.cosigner.co_signer_converter import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestCoSigner:

    def test_co_signer_converter(self):
        config = read_yaml("./config.yaml")
        converter = CoSignerConverter(config)
        # The CoSignerCallBack received by the controller
        # Visit the following link to view the request data specification：https://docs.safeheron.com/api/en.html#API%20Co-Signer%20Request%20Data
        co_signer_call_back = {}
        biz_content = converter.request_v3_convert(co_signer_call_back)
        # According to different types of CoSignerCallBack, the customer handles the corresponding type of business logic.
        print(biz_content)

        # Visit the following link to view the response data specification.：https://docs.safeheron.com/api/en.html#Approval%20Callback%20Service%20Response%20Data
        coSignerResponse = CoSignerResponseV3()
        coSignerResponse.action = "<Replace with APPROVE or REJECT>"
        coSignerResponse.approvalId = "<Replace with the approvalId data from the request>"
        encryptResponse = converter.response_v3_converter(coSignerResponse)
        # The customer returns encryptResponse after processing the business logic.
