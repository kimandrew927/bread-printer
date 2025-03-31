import requests
from bs4 import BeautifulSoup
import re

# Replace this with the URL of the product you're tracking
url = "https://www.amazon.com/Ringside-Mexican-Style-Boxing-Handwrap-180-Inch/dp/B00CHV2VB6/ref=sr_1_8?crid=1BZSDSUIWHQGP&dib=eyJ2IjoiMSJ9.gN2-mVk9AMaRXYTchd_mdT-DkO1sa8thPPF90WtL8eU6lVfE9kE7TC-0ZReIVes5QBTiHIg48xfYp14yPTNRxxRzQOZmbNVBTG_4XsxFzC266HOUuWTB8bVrL-5c2umxbmoakX84xqaX4GWP4jAJPVh9XQKrXCeJ-cZD1q4XTY4xMyM_X6XAAwegGSiM2RNVxzTtgoo2-e-znR_9W5qN61Ud_lrBoSB9LIk-zxwduP1BoM0bFqHi_UQV5he7jl1kkMuyQLcn_HO8_QSiYUG-6_A3B8D7rbbJKzLS6aT3Sw8kGcEvvxrmo4F7vWdAfIe7IjBcEogmYbyx_qHncD6r8oiV2DEOgOj7aSg3gSgGeOVZl0ed2ph-9Ho9znG17QsiChcE9D8H8fy8sgiKw5zJv1WRKBCidOe_n2poJCji71_DyASvWsY_2DIeaCHD_3Ye.ww9x6pbfCEDhd_Jwc9NtU6dfjFJnO86uNchQSlp48y0&dib_tag=se&keywords=boxing%2Bhand%2Bwraps&qid=1743444243&sprefix=boxing%2Bhand%2Bwraps%2Caps%2C83&sr=8-8&th=1"  # Example product URL

# User-Agent string to avoid being blocked by Amazon
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

def get_amazon_price(url):
    try:
        headers = {
        "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",  
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            print(soup.title)
            price = None
            price_selectors = [
                {"id": "priceblock_ourprice"},
                {"id": "priceblock_dealprice"},
                {"id": "price_inside_buybox"},
                {"class_": "a-offscreen"}  # fallback for some formats
            ]
            
            for selector in price_selectors:
                element = soup.find("span", **selector)
                if element:
                    price_text = element.text.strip()
                    price = re.sub(r'[^\d.]', '', price_text)
                    
                    break

            if price:
                return float(price)
            else:
                print("Couldn't find price on the page.")
                return None
        else:
            print(f"Failed to retrieve page. Status code: {response.status_code}")
            return None
    except requests.exceptions.Timeout:
        print("Request timed out.")
        return None

# Test the function
price = get_amazon_price(url)
if price:
    print(f"The current price of the product is ${price}")