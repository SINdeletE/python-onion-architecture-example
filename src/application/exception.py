class ApplicationError(Exception):
    """Base error exposed by application operations."""


class NotFoundError(ApplicationError):
    """The requested resource does not exist (HTTP equivalent: 404)."""


class ConflictError(ApplicationError):
    """The operation conflicts with existing data (HTTP equivalent: 409)."""


class UnprocessableEntityError(ApplicationError):
    """The supplied data cannot be processed (HTTP equivalent: 422)."""


class InternalServerError(ApplicationError):
    """An unexpected internal failure occurred (HTTP equivalent: 500)."""


class ServiceUnavailableError(ApplicationError):
    """A required service is unavailable (HTTP equivalent: 503)."""
