class ArgillaAPIError(Exception):
    pass


class BadRequestError(ArgillaAPIError):
    pass


class ForbiddenError(Exception):
    pass


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class UnprocessableEntityError(Exception):
    pass


class InternalServerError(Exception):
    pass
