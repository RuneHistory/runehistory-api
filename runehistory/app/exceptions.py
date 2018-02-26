class RHError(Exception):
    pass


class AdapterError(Exception):
    pass


class DuplicateError(RHError):
    pass


class NotFoundError(RHError):
    pass
