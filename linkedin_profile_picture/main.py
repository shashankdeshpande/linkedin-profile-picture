import re
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

    def _extract_linkedin_results(self, res: list) -> dict:
        img_dict = {}
        for i in res:
            context_url = i.get("image",{}).get("contextLink","")
            pic_url = i.get("link","")
            if self._check_linkedin_id(context_url) and self._check_picture_url(pic_url):
                linkedin_id = self.clean_id(context_url)
                img_dict[linkedin_id] = pic_url
        return img_dict

    def search(self, params: dict) -> dict:
        res = self._api_obj._hit_api(params)
        res = res.get("items",[])
        res = self._extract_linkedin_results(res)
        return res
