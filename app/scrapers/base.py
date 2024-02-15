import abc


class BaseScraperClient(abc.ABC):

    @abc.abstractmethod
    def search_by_name(self, name) -> list:
        raise NotImplementedError("search_by_name method is not implemented")
