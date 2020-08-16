#
# Create the API context based on the provided arguments
#

import dateutil.parser
import v20

from spideroptic.ext.oanda.candle import Candle

api = v20.Context(
    "api-fxtrade.oanda.com",
    token=""
)


def get_instruments():
    response = api.account.instruments(accountID="")
    if response.status != 200:
        print(response)
        print(response.body)

    return response.get("instruments", 200)


def get_candles(period="D", instrument="USD_JPY", start=None, end=None):
    kwargs = {}

    kwargs["price"] = "M"
    kwargs["granularity"] = period
    kwargs["count"] = 5000
    if start:
        kwargs["fromTime"] = start
    if end:
        kwargs["toTime"] = end

    response = api.instrument.candles(instrument, **kwargs)
    if response.status != 200:
        print(response)
        print(response.body)

    return response.get("candles")


def get_order_book(instrument="USD_JPY"):
    kwargs = {}

    #kwargs["time"] = "M"

    response = api.instrument.order_book(instrument, **kwargs)
    if response.status != 200:
        print(response)
        print(response.body)

    return response.get("orderBook", 200)


def get_position_book(instrument="USD_JPY"):
    kwargs = {}

    #kwargs["time"] = "M"

    response = api.instrument.position_book(instrument, **kwargs)
    if response.status != 200:
        print(response)
        print(response.body)

    return response.get("positionBook", 200)


def prepare_cadles(candles):
    candle_records = []

    for candle in candles:
        candle_records.append(Candle(date=candle.time, open=getattr(candle, 'mid', None).o, high=getattr(candle, 'mid', None).h, low=getattr(candle, 'mid', None).l, close=getattr(candle, 'mid', None).c))

    return candle_records
