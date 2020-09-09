import re
import requests
from urllib.parse import urlparse
from .google_search_api import GoogleSearchAPI

class ProfilePicture(object):

    def __init__(self, key: str, cx: str):
        self._api_obj = GoogleSearchAPI(key, cx)

    def extract_id(self, link: str) -> str:
        """
            To get clean linkedin id
            Example: 
                Input  : linkedin.com/in/shashank-deshpande/
                Output : shashank-deshpande
        """
        linkedin_id = link
        match = re.findall(r'\/in\/([^\/]+)\/?', urlparse(link).path)
        if match:
            linkedin_id = match[0].strip()
        linkedin_id = linkedin_id.strip("/")
        return linkedin_id

    def _check_picture_url(self, link: str) -> bool:
        match = re.findall(r"(media-exp\d\.licdn\.com).+?(profile-displayphoto-shrink_)", link)
        return bool(match)

    def _check_url_exists(self, link):
        flag = False
        try:
            resp = requests.get(link, timeout=5)
            if resp and resp.status_code == 200:
                flag = True
        except:
            pass
        return flag

    def _extract_profile_picture(self, linkedin_id: str, res: list) -> str:
        link = ""
        for i in res:
            linkedin_url = i.get("link","")
            search_id = self.extract_id(linkedin_url)
            if search_id == linkedin_id:
                metatags = i.get("pagemap",{}).get("metatags", [])
                metatags = sum(list(map(lambda mt: list(dict(filter(lambda x: "image" in x[1], mt.items())).values()), metatags)), [])

                cse_imgs = i.get("pagemap",{}).get("cse_image", [])
                cse_imgs = list(filter(None, map(lambda x:x.get("src"), cse_imgs)))

                pic_urls = set(metatags + cse_imgs)
                for url in pic_urls:
                    if self._check_picture_url(url) and self._check_url_exists(url):
                        link = url
                        break
            if link:
                break
        return link

    def search(self, params: dict) -> object:
        linkedin_id = self.extract_id(params.get("q",""))
        api_resp = self._api_obj._hit_api(params)
        api_resp.link = self._extract_profile_picture(linkedin_id, api_resp._search_results)
        return api_resp
