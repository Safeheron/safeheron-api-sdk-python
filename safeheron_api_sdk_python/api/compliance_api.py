from safeheron_api_sdk_python.client import *


class KytReportRequest:
    def __init__(self):
        # Transaction Key. Cannot be empty at the same time as customerRefId. If both are provided, txKey takes precedence
        self.txKey = None
        # Merchant unique business ID (100 characters max)
        self.customerRefId = None


class CreateKyaScreeningRequest:
    def __init__(self):
        # On-chain address to screen (not limited to Safeheron addresses)
        self.address = None
        # Chain type. See "Retrieve Supported Networks & Providers" for valid values
        self.chainType = None
        # Blockchain network identifier. Required when providers contains MistTrack
        self.network = None
        # Screening providers — at least one, no duplicates, screened in parallel. Valid values: MistTrack, Elliptic, Chainalysis
        self.providers = None


class KyaScreeningOneRequest:
    def __init__(self):
        # Screening request ID
        self.screenId = None


class KyaScreeningOrderOneRequest:
    def __init__(self):
        # Screening order ID
        self.screenOrderId = None


class KyaSupportedNetworksRequest:
    def __init__(self):
        pass


class ComplianceApi:

    def __init__(self, config):
        self.api_client = Client(config)

    # Retrieve Transaction KYT Report
    def kyt_report(self, request: KytReportRequest):
        return self.api_client.send_request(request, '/v1/compliance/kyt/report')

    # Create KYA Screening Request
    # Initiates an address screening request against one or more AML providers in parallel
    def create_kya_screening(self, request: CreateKyaScreeningRequest):
        return self.api_client.send_request(request, '/v1/compliance/kya/screening/create')

    # Retrieve KYA Screening Summary
    # Returns the overall status and per-order results for a screening request
    def kya_screening_one(self, request: KyaScreeningOneRequest):
        return self.api_client.send_request(request, '/v1/compliance/kya/screening/one')

    # Retrieve KYA Screening Order Details
    # Returns the detailed result of a single provider screening order, including the raw provider payload
    def kya_screening_order_one(self, request: KyaScreeningOrderOneRequest):
        return self.api_client.send_request(request, '/v1/compliance/kya/screening/order/one')

    # Retrieve Supported Networks & Providers
    # Returns the list of blockchain networks and the AML providers that support each network
    def kya_supported_networks(self):
        return self.api_client.send_request(KyaSupportedNetworksRequest(), '/v1/compliance/kya/supportedNetworks')
