import requests

from app.scrapers.base import BaseScraperClient

regions = {
    "Artigas": "U1cjdGF0YXV5YXJ0aWdhcw==",
    "Colonia": "U1cjdGF0YXV5Y29sb25pYTt0YXRhdXlzZWxsZXJjcm9zc21lcmNhZG8",
    "Durazno": "U1cjdGF0YXV5ZHVyYXpubw==",
    "Florida": "U1cjdGF0YXV5ZmxvcmlkYQ==",
    "Maldonado": "",
    "Melo": "",
    "Mercedes": "",
    "Minas": "",
    "Montevideo": "U1cjdGF0YXV5bW9udGV2aWRlbw==",
    "Ciudad de la Costa": "U1cjdGF0YXV5bW9udGV2aWRlbw==",
    "La Paz": "",
    "Las Piedras": "",
    "Payasandu": "",
    "Rivera": "",
    "Salto": "",
    "Tacuarembo": "",
}


class TaTaScraperClient(BaseScraperClient):

    def __init__(self):
        self.regions = regions
        self.provider = "TaTa"
        self.base_url = "https://www.tata.com.uy/"

    def search_by_name(self, name: str) -> list:

        referer = f"{self.base_url}s/?q={name}&sort=score_desc&page=0"

        headers = {
            "authority": "www.tata.com.uy",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9,es;q=0.8",
            "referer": referer,
            "sec-ch-ua": '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/121.0.0.0 Safari/537.36",
        }
        params = {
            "operationName": "ProductsQuery",
            "variables": '{"first":16,"after":"0","sort":"score_desc","term":"%s","selectedFacets":[{"key":"channel",'
            % name
            + '"value":"{\\"salesChannel\\":\\"4\\",\\"regionId\\":\\"%s\\"}"},'
            % self.regions["Montevideo"]
            + '{"key":"locale","value":"es-UY"}]}',
        }
        response = requests.get(
            "https://www.tata.com.uy/api/graphql", params=params, headers=headers
        ).json()

        edges = response["data"]["search"]["products"]["edges"]
        products = []
        for edge in edges:
            node = edge["node"]
            price = {
                "amount": node["offers"]["lowPrice"],
                "currency": "UYU",
                "decimal_places": 0,
            }
            product_data = {
                "name": node["name"],
                "regular_price": price,
                "discount_price": price,
                "redirect_url": "tata.com.uy",
                "provider": "TaTa",
            }
            products.append(product_data)
        return products
