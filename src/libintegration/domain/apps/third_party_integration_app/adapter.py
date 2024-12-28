from fastapi import status


class ThirdPartyAdapter:
    
    @staticmethod
    def build_request():
        return {}

    @staticmethod
    def parse_response(response):
        if response.status_code == status.HTTP_200_OK:
            response = response.json()
            return response.get("data")
        
        return response
