import abc
import dataclasses
import logging


@dataclasses.dataclass
class BaseScraperClient(abc.ABC):
    provider: str

    def __init__(self):
        logging.log(logging.INFO, f"Scraper with provider {self.provider} was created")
        pass

    @abc.abstractmethod
    async def search_by_name(self, name) -> list:
        raise NotImplementedError("search_by_name method is not implemented")
