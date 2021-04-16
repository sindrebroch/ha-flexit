"""Exceptions for Flexit."""
"""Move to library"""

class FlexitError(Exception):
    """Generic Flexit exception."""

    pass


class FlexitConnectionError(FlexitError):
    """Flexit connection exception."""

    pass
