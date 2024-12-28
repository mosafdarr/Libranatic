from logger import logger
from libintegration.domain.apps.third_party_integration_app.base import ThirdPartyBase, third_party_exception_handler
from libintegration.domain.abstraction.third_party_abstract import ThirdPartyAbstract
from libintegration.domain.apps.third_party_integration_app.adapter import ThirdPartyAdapter
from libintegration.libcommon.http_client import HTTPClient


class ThirdPartyIntegration(ThirdPartyBase, ThirdPartyAbstract):
    @third_party_exception_handler
    def get(self, param: str):
        logger.info(f"Test Third Party Integration - {param}")
        url = "/get-company-posts?username=microsoft&start=0"
        request_payload = ThirdPartyAdapter.build_request()
        response = HTTPClient(self.base_url).get(endpoint=url, headers=self.get_header())
        parse_response = ThirdPartyAdapter.parse_response(response)

        return parse_response
