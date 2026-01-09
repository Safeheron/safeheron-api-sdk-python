from safeheron_api_sdk_python.client import *


class KytReportRequest:
    def __init__(self):
        # Blockchain network, supports:
        # Bitcoin
        # Ethereum
        # Tron
        self.txKey = None
        # Address
        self.customerRefId = None


class ComplianceApi:

    def __init__(self, config):
        self.api_client = Client(config)

    # Create AML Risk Assessment Request
    def kyt_report(self, request: KytReportRequest):
        return self.api_client.send_request(request, '/v1/compliance/kyt/report')
