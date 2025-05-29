from safeheron_api_sdk_python.client import *


class AmlCheckerRequestRequest:
    def __init__(self):
        # Blockchain network, supports:
        # Bitcoin
        # Ethereum
        # Tron
        self.network = None
        # Address
        self.address = None


class AmlCheckerRetrievesRequest:
    def __init__(self):
        # Risk assessment request ID, which can be created through the Create AML Risk Assessment Request interface.
        self.requestId = None


class ToolsApi:

    def __init__(self, config):
        self.api_client = Client(config)

    # Create AML Risk Assessment Request
    def aml_checker_request(self, request: AmlCheckerRequestRequest):
        return self.api_client.send_request(request, '/v1/tools/aml-checker/request')

    # Retrieve AML Risk Assessment Result
    def aml_checker_retrieves(self, request: AmlCheckerRetrievesRequest):
        return self.api_client.send_request(request, '/v1/tools/aml-checker/retrieves')
