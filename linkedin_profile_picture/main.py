import re
import requests
from .google_search_api import GoogleSearchAPI

class ProfilePicture(object):

    def __init__(self, key: str, cx: str):
        self._api_obj = GoogleSearchAPI(key, cx)

    def clean_id(self, link: str) -> str:
        """
            To get clean linkedin id
            Example: 
                Input  : linkedin.com/in/shashank-deshpande/
                Output : shashank-deshpande
        """
        match = re.findall(r'in\/([^\/]+)\/?', link)
        linkedin_id = match[0].strip() if match else link
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
            pic_url = i.get("link","")
            context_url = i.get("image",{}).get("contextLink","")
            res_lid = self.clean_id(context_url)
            if linkedin_id == res_lid and self._check_picture_url(pic_url) and self._check_url_exists(pic_url):
                link = pic_url
                break
        return link

    def search(self, params: dict) -> object:
        linkedin_id = self.clean_id(params.get("q",""))
        api_resp = self._api_obj._hit_api(params)
        api_resp.link = self._extract_profile_picture(linkedin_id, api_resp._search_results)
        return api_resp
