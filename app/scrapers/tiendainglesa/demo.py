from typing import List
from bs4 import BeautifulSoup

import requests

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


if __name__ == "__main__":
    perform_search("tv")
