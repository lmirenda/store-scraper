import asyncio

from app.schemas.product import Product
from app.scrapers.base import BaseScraperClient

from app.scrapers.devoto.client import DevotoScraperClient
from app.scrapers.disco.client import DiscoScraperClient
from app.scrapers.geant.client import GeantScraperClient
from app.scrapers.tata.client import TaTaScraperClient
from app.scrapers.tiendainglesa.client import TiendaInglesaScraperClient


class ProductRepository:
    scraper_clients: list[BaseScraperClient]

    def __init__(self):
        self.set_scrapers()

    def set_scrapers(self) -> None:
        tienda_inglesa = TiendaInglesaScraperClient()
        tata = TaTaScraperClient()
        geant = GeantScraperClient()
        devoto = DevotoScraperClient()
        disco = DiscoScraperClient()
        self.scraper_clients = [tata, geant, disco, tienda_inglesa]

    @staticmethod
    async def fetch_and_store_results(
        scraper: BaseScraperClient, name: str, results: list
    ):
        product_list = await scraper.search_by_name(name)
        first_5_products = product_list[:5]
        results.extend(first_5_products)

    async def get_by_name(self, name: str) -> list[Product]:

        all_products = []
        tasks = [
            self.fetch_and_store_results(scraper, name, all_products)
            for scraper in self.scraper_clients
        ]
        await asyncio.gather(*tasks)

        return all_products
