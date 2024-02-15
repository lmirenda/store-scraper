import asyncio
import json

import requests

from app.scrapers.base import BaseScraperClient


class GeantScraperClient(BaseScraperClient):

    provider = "Geant"
    base_url = "https://www.geant.com.uy/"

    def __init__(self):
        super().__init__()

    async def search_by_name(self, name: str) -> list:

        await asyncio.sleep(1)

        headers = {
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "accept": "application/json",
            "sec-ch-ua-mobile": "?0",
        }

        params = {
            "_q": "{}".format(name),
            "map": "ft",
            "__pickRuntime": "appsEtag,blocks,blocksTree,components,contentMap,extensions,messages,page,pages,query,queryData,route,runtimeMeta,settings",
        }

        response = requests.get(
            "{}{}".format(self.base_url, name), params=params, headers=headers
        )
        rsp = response.json()

        product_list = []
        products_str = rsp["queryData"][0]["data"]
        products_dict = json.loads(products_str)

        products = products_dict["productSearch"]["products"]

        for product in products:

            discount_price = {
                "amount": product["priceRange"]["sellingPrice"]["lowPrice"],
                "currency": "UYU",
                "decimal_places": 0,
            }

            regular_price = {
                "amount": product["priceRange"]["sellingPrice"]["highPrice"],
                "currency": "UYU",
                "decimal_places": 0,
            }

            product_data = {
                "name": product["productName"],
                "redirect_url": product["link"],
                "provider": self.provider,
                "regular_price": regular_price,
                "discount_price": discount_price,
            }
            product_list.append(product_data)

        return product_list
