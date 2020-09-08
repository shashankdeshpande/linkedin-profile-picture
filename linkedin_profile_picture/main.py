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
        match = self._check_linkedin_id(link)
        linkedin_id = match[0].strip() if match else link
        linkedin_id = linkedin_id.strip("/")
        return linkedin_id

    def _check_linkedin_id(self, link: str):
        match = re.findall(r'in\/([^\/]+)\/?', link)
        return match

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

    def _extract_linkedin_results(self, res: list) -> dict:
        img_dict = {}
        for i in res:
            pic_url = i.get("link","")
            thumbnail = i.get("image",{}).get("thumbnailLink","")
            context_url = i.get("image",{}).get("contextLink","")

            if self._check_linkedin_id(context_url) and self._check_picture_url(pic_url):
                priority = filter(None, [pic_url, thumbnail])
                for url in priority:
                    if self._check_url_exists(url):
                        linkedin_id = self.clean_id(context_url)
                        img_dict[linkedin_id] = pic_url
                        break
        return img_dict

    def search(self, params: dict) -> dict:
        res = self._api_obj._hit_api(params)
        res = res.get("items",[])
        res = self._extract_linkedin_results(res)
        return res
