import asyncio
import re

from bs4 import BeautifulSoup

import requests
from pyppeteer import launch

from app.schemas.money import Money
from app.schemas.product import Product


def perform_search(name: str) -> list:

    str.replace(name, " ", "+")

    headers = {
        "authority": "www.tiendainglesa.com.uy",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9,es;q=0.8",
        # 'cookie': 'GX_CLIENT_ID=489ac49e-056a-4236-aa3c-6c04b64eb5b4; GX_SESSION_ID=GjSjnPaG6M5%2BTYgMrUA4910CwxHOBIB%2BmwNdvLButT8%3D; TI_STORE=100219; rrpvid=574787581229714; auth=0; JSESSIONID=63FB1576626023FC568DFCEF3DFE70CE; TI_LOADEDLANDING=Y; rr-testCookie=testvalue; AWSALB=BYma5Gx49qyUlFdoeGqgNoLnoOUiALXd8o2I4rYULvGyvmf4TrWeiTMdx5Fy6DjtGlynHGWvVbUfCU1X5cBhC4fyD9dlJ2feYaO1eOk1Ymvp1jIJxFDH26YyWAQu; AWSALBCORS=BYma5Gx49qyUlFdoeGqgNoLnoOUiALXd8o2I4rYULvGyvmf4TrWeiTMdx5Fy6DjtGlynHGWvVbUfCU1X5cBhC4fyD9dlJ2feYaO1eOk1Ymvp1jIJxFDH26YyWAQu',
        "referer": f"https://www.tiendainglesa.com.uy/supermercado/busqueda?0,0,{name},0",
        "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    response = requests.get(
        f"https://www.tiendainglesa.com.uy/supermercado/busqueda?0,0,{name},0",
        headers=headers,
    )

    soup = BeautifulSoup(response.text, "html.parser")

    products = soup.body.find_all(class_="card-product-name-and-price")

    product_list = []
    for product in products:
        product_name = product.find(class_="card-product-name").text
        product_price = product.find(class_="card-product-price").text
        img = product.find("a")["href"]
        product_item = Product(name=product_name, price=product_price, image=img)
        product_list.append(product_item)

    print(product_list)

    return product_list


async def perform_search_async(name: str) -> list[Product]:
    url = f"https://www.tiendainglesa.com.uy/supermercado/busqueda?0,0,{name},0"
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)

    products = await page.querySelectorAll(".card-product-name-and-price")
    product_list = []
    for product in products:
        product_name = await product.querySelectorEval(
            ".card-product-name", "e => e.textContent"
        )
        product_price = await product.querySelectorEval(
            ".card-product-price", "e => e.textContent"
        )
        product_price = extract_price(product_price)
        redirect_url = await product.querySelectorEval("a", "e => e.href")
        product_item = Product(
            name=product_name,
            regular_price=product_price[0],
            discount_price=product_price[1],
            redirect_url=redirect_url,
            provider="Tienda Inglesa",
        )
        product_list.append(product_item)

    print(product_list)

    await browser.close()

    return product_list


def extract_price(price: str) -> tuple:
    price = str.replace(price, "\t", "")

    usd_pattern = r"U\$\S\s\d+"
    uyu_pattern = r"\$\s\d+"

    usd_matches = re.findall(usd_pattern, price)
    uyu_matches = re.findall(uyu_pattern, price)

    if usd_matches:
        if len(usd_matches) > 1:
            regular_price = Money(
                amount=usd_matches[0].split(" ")[1], currency="USD", decimal_places=0
            )
            discount_price = Money(
                amount=usd_matches[1].split(" ")[1], currency="USD", decimal_places=0
            )
        else:
            regular_price = Money(
                amount=usd_matches[0].split(" ")[1], currency="USD", decimal_places=0
            )
            discount_price = Money(
                amount=usd_matches[0].split(" ")[1], currency="USD", decimal_places=0
            )
    elif uyu_matches:
        if len(uyu_matches) > 1:
            regular_price = Money(
                amount=uyu_matches[0].split(" ")[1], currency="UYU", decimal_places=0
            )
            discount_price = Money(
                amount=uyu_matches[1].split(" ")[1], currency="UYU", decimal_places=0
            )
        else:
            regular_price = Money(
                amount=uyu_matches[0].split(" ")[1], currency="UYU", decimal_places=0
            )
            discount_price = Money(
                amount=uyu_matches[0].split(" ")[1], currency="UYU", decimal_places=0
            )
    else:
        raise ValueError("Price not found")

    return regular_price, discount_price


if __name__ == "__main__":
    # perform_search("fideos")
    asyncio.run(perform_search_async("tv"))
