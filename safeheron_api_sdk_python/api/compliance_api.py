from safeheron_api_sdk_python.client import *


class KytReportRequest:
    def __init__(self):
        # Transaction Key. Cannot be empty at the same time as customerRefId. If both are provided, txKey takes precedence
        self.txKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None


class ComplianceApi:

    def __init__(self, config):
        self.api_client = Client(config)

    # Retrieve Transaction KYT Report
    def kyt_report(self, request: KytReportRequest):
        return self.api_client.send_request(request, '/v1/compliance/kyt/report')
