class PaginationQuery:
    def __init__(self, page: int = 1, limit: int = 10):
        self.page = page
        self.limit = limit

    def __call__(self, page, limit):
        self.page = page
        self.limit = limit
        return self
