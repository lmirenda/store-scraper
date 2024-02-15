import re
from pyppeteer import launch

from app.schemas.money import Money
from app.scrapers.base import BaseScraperClient


class TiendaInglesaClient(BaseScraperClient):

    async def search_by_name(self, name: str) -> list:
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
            product_price = self._extract_price(product_price)
            redirect_url = await product.querySelectorEval("a", "e => e.href")
            product_item = dict(
                name=product_name,
                regular_price=product_price[0],
                discount_price=product_price[1],
                redirect_url=redirect_url,
                provider="Tienda Inglesa",
            )
            product_list.append(product_item)

        await browser.close()

        return product_list

    @staticmethod
    def _extract_price(price: str) -> tuple:
        price = str.replace(price, "\t", "")

        usd_pattern = r"U\$\S\s\d+"
        uyu_pattern = r"\$\s\d+"

        usd_matches = re.findall(usd_pattern, price)
        uyu_matches = re.findall(uyu_pattern, price)

        if usd_matches:
            if len(usd_matches) > 1:
                regular_price = Money(
                    amount=usd_matches[0].split(" ")[1],
                    currency="USD",
                    decimal_places=0,
                )
                discount_price = Money(
                    amount=usd_matches[1].split(" ")[1],
                    currency="USD",
                    decimal_places=0,
                )
            else:
                regular_price = Money(
                    amount=usd_matches[0].split(" ")[1],
                    currency="USD",
                    decimal_places=0,
                )
                discount_price = Money(
                    amount=usd_matches[0].split(" ")[1],
                    currency="USD",
                    decimal_places=0,
                )
        elif uyu_matches:
            if len(uyu_matches) > 1:
                regular_price = Money(
                    amount=uyu_matches[0].split(" ")[1],
                    currency="UYU",
                    decimal_places=0,
                )
                discount_price = Money(
                    amount=uyu_matches[1].split(" ")[1],
                    currency="UYU",
                    decimal_places=0,
                )
            else:
                regular_price = Money(
                    amount=uyu_matches[0].split(" ")[1],
                    currency="UYU",
                    decimal_places=0,
                )
                discount_price = Money(
                    amount=uyu_matches[0].split(" ")[1],
                    currency="UYU",
                    decimal_places=0,
                )
        else:
            raise ValueError("Price not found")

        return regular_price, discount_price
