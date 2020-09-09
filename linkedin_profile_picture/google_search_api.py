import requests
import logging

logger = logging.getLogger(__name__)

class GoogleSearchAPI:

    def __init__(self, key: str, cx: str):
        self._cx = cx
        self._key = key
        self._api_url = "https://www.googleapis.com/customsearch/v1"
        self._params = {
            "num": 10,
            "searchType": "image"
            }

    def _hit_api(self, params):
        api_response = APIResponse()
        try:
            params = dict(params, **self._params)
            params["cx"] = self._cx
            params["key"] = self._key
            resp = requests.get(self._api_url, params=params)
            api_response = self._create_api_response(resp)
        except Exception as e:
            logger.info(f"Error in _hit_api: {e}", exc_info=True)
        return api_response

    def _create_api_response(self, resp):
        link = ""
        results = []
        error = None
        status_code = resp.status_code
        if status_code == 200:
            results = resp.json()
            results = results.get("items",[])
        else:
            error = resp.json()
        return APIResponse(results, status_code, link, error)

class APIResponse:

    def __init__(self,
            _search_results=[],
            status_code=400,
            link="",
            error=None):
        self._search_results = _search_results
        self.status_code = status_code
        self.link = link
        self.error = error
