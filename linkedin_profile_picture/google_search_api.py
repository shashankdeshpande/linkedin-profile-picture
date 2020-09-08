import requests
import logging

logger = logging.getLogger(__name__)

class GoogleSearchAPI(object):

    def __init__(self, key: str, cx: str):
        self._cx = cx
        self._key = key
        self._api_url = "https://www.googleapis.com/customsearch/v1"
        self._params = {
            "num": 10,
            "searchType": "image"
            }

    def _hit_api(self, params):
        api_response = {}
        try:
            params = dict(params, **self._params)
            params["cx"] = self._cx
            params["key"] = self._key
            resp = requests.get(self._api_url, params=params)
            if resp and resp.status_code == 200 and "json" in dir(resp):
                api_response = resp.json()
        except Exception as e:
            logger.info(f"Error in _hit_api: {e}", exc_info=True)
        return api_response
