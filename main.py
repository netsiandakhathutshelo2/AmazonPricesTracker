from bs4 import BeautifulSoup
import requests
from smtplib import SMTP
import datetime
import os
from dotenv import load_dotenv

load_dotenv()
url = "https://appbrewery.github.io/instant_pot/"
response = requests.get(url)
Soup = BeautifulSoup(response.text, "html.parser")

# Find the HTML element that contains the price
price_whole = Soup.find(name="span", class_="a-price-whole")
price_fraction = Soup.find(name="span", class_="a-price-fraction")
price = float(f"{price_whole.get_text()}{price_fraction.get_text()}")

target_price = 100
title_product = (Soup.find(name="span", id="productTitle", class_="a-size-large product-title-word-break")).get_text()
# link_product = Soup.find(name="a", class_="a-price-fraction")

if target_price <= 100:

    with SMTP("smtp.office365.com", port=587) as smtp:
        smtp.starttls()
        result = smtp.login(os.environ["SMTP_ADDRESS"], os.environ["EMAIL_PASSWORD"])
        date = datetime.datetime.now()
        message = f"Hey There!! {title_product} is on sale for Price:{price}\nLink:{url}"
        smtp.sendmail(from_addr=os.environ["SMTP_ADDRESS"],
                      to_addrs=os.environ["EMAIL_ADDRESS"],
                      msg=f"Subject:Amazon Price Alert!!!\n\n{message}".encode("utf-8"))
