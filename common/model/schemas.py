from pydantic import BaseModel, BaseSettings, validator, root_validator
from typing import Literal

CRYPTO_LITERAL = Literal["BINANCE", "UPBIT"]

EXCHANGE_LITERAL = Literal["BINANCE", "UPBIT"]

QUOTE_LITERAL = Literal["USDT", "USDT.P", "USDTPERP", "KRW"]

SIDE_LITERAL = Literal["buy", "sell", "entry/buy", "entry/sell", "close/buy", "close/sell"]

CRYPTO_EXCHANGES = ("BINANCE", "UPBIT")

crypto_futures_code = ("PERP", ".P")


def parse_side(side: str):
    if side.startswith("entry/") or side.startswith("close/"):
        return side.split("/")[-1]
    else:
        return side

def parse_quote(quote: str):
    if quote.endswith(".P"):
        return quote.replace(".P", "")
    else:
        return quote
