import yaml
import sys

sys.path.append('../../../../safeheron-api-sdk-python')
from safeheron.webhook.webhook_converter import *


def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


class TestWbeHook:
    def test_co_signer_converter(self):
        config = read_yaml("./config.yaml")
        converter = WebhookConverter(config)
        # The CoSignerCallBack received by the controller
        webhook = {}
        biz_content = converter.converter(webhook)
        # According to different types of WebHook, the customer handles the corresponding type of business logic.
        print(biz_content)

        webHookResponse = {'message': 'SUCCESS', 'code': '200'}
        # The customer returns WebHookResponse after processing the business logic.
