"""Exceptions for Flexit."""


class FlexitError(Exception):
    """Generic Flexit exception."""

    pass


class FlexitConnectionError(FlexitError):
    """Flexit connection exception."""

    pass
