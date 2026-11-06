class InsufficientFundsError(Exception):
    """Недостаточно средств."""


class CurrencyNotFoundError(Exception):
    """Неизвестная валюта."""


class ApiRequestError(Exception):
    """сбой внешнего API."""
