# amazon_reviews.py
import requests
import re
from json import JSONDecodeError

API_BASE = "https://api.scrapingdog.com/amazon-reviews"  # endpoint must be this path

def extract_asin_from_url(url: str) -> str | None:
    if not url:
        return None
    for pat in (r"/dp/([A-Z0-9]{10})", r"/gp/product/([A-Z0-9]{10})", r"/([A-Z0-9]{10})(?:[/?]|$)"):
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None

def fetch_amazon_reviews(amazon_url: str, api_key: str, max_reviews: int = 40):
    asin = extract_asin_from_url(amazon_url or "")
    import requests
    url = "https://api.scrapingdog.com/amazon/product"
    params = {
        "api_key": api_key,
        "asin": asin,
        "domain": "in",
        "postal_code": "",
        "country": "us"
    }
    response = requests.get(url, params=params)
    reviews = []
    if response.status_code == 200:
        data = response.json()
        c_reviews = data["customer_reviews"]
        for c in c_reviews:
            reviews.append(c["review_snippet"])
    else:
        print(f"Request failed with status code: {response.status_code}")
    return reviews[:max_reviews], None

if __name__ == "__main__":
    url = "https://www.amazon.in/Redmi-Starlight-Storage-Superfast-Snapdragon/dp/B0DQV9T66N/ref=pd_ci_mcx_mh_mcx_views_0_image?pd_rd_w=ydIVY&content-id=amzn1.sym.1710d64e-6f05-4654-b067-ac772d543749%3Aamzn1.symc.ca948091-a64d-450e-86d7-c161ca33337b&pf_rd_p=1710d64e-6f05-4654-b067-ac772d543749&pf_rd_r=NCP9AKZK139G1GMT859G&pd_rd_wg=M89Le&pd_rd_r=f79a7dfa-83bc-4f42-a075-ee8cc55b92f5&pd_rd_i=B0DQV9T66N"
    print(fetch_amazon_reviews(url, "6895946634fc643e278c4436"))
