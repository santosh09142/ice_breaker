import os
import requests
from dotenv import load_dotenv
from sqlalchemy import false

load_dotenv()


def scrape_linkdin_profile(linkdin_profile_url: str, mock: bool=False):
    """scrape information from Linkdin profiles,
    Manually scrape the information from the Linkdin profile """
    if mock:
        print("In Mock")
        linkdin_profile_url = "https://gist.githubusercontent.com/santosh09142/ab8200e8c5ceb92e5ca64e727ce7b15f/raw/d0a7caa58c8c895bd69e0b5e8fde98c2d7de0060/santosh.json"
        response = requests.get(
            linkdin_profile_url,
            timeout=10,
        )
        print(response)
    else:
        headers = {'Authorization': f'Bearer {os.environ.get("PROXYCURL_API_KEY")}' }
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'

        response = requests.get(
            api_endpoint,
            params={'url': linkdin_profile_url},
            headers=headers,
            timeout=10,
        )
    data = response.json()
    data = {
        k: v
        for k, v in data.items()
        if v not in ([],"", "", None)
        and k not in ["people_also_viewed","certifications"]
    }
    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")

    return data



