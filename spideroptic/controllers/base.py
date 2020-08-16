
from cement import Controller, ex
from cement.utils.version import get_version_banner
import asciiplotlib as apl
import numpy as np
from spideroptic.ext.oanda.wrapper import get_candles, prepare_cadles
from ..core.version import get_version

VERSION_BANNER = """
Spider Optic forex guider %s
%s
""" % (get_version(), get_version_banner())


class Base(Controller):

    symbols = [
        "EUR_USD", "EUR_GBP", "EUR_AUD", "EUR_NZD", "EUR_JPY", "EUR_CHF", "EUR_CAD",
        "EUR_USD", "GBP_USD", "AUD_USD", "NZD_USD", "USD_JPY", "USD_CHF", "USD_CAD",
        "EUR_GBP", "GBP_USD", "GBP_AUD", "GBP_NZD", "GBP_JPY", "GBP_CHF", "GBP_CAD",
        "EUR_JPY", "USD_JPY", "AUD_JPY", "NZD_JPY", "GBP_JPY", "CHF_JPY", "CAD_JPY",
        "EUR_AUD", "AUD_USD", "AUD_JPY", "AUD_NZD", "GBP_AUD", "AUD_CHF", "AUD_CAD",
        "EUR_NZD", "NZD_USD", "AUD_NZD", "NZD_JPY", "GBP_NZD", "NZD_CHF", "NZD_CAD",
        "EUR_CHF", "NZD_CHF", "AUD_CHF", "CHF_JPY", "GBP_CHF", "USD_CHF", "CAD_CHF",
        "EUR_CAD", "USD_CAD", "AUD_CAD", "NZD_CAD", "GBP_CAD", "CAD_CHF", "CAD_JPY"
    ]

    weights = [
        1, 1, 1, 1, 1, 1, 1,
        -1, -1, -1, -1, 1, 1, 1,
        -1, 1, 1, 1, 1, 1, 1,
        -1, -1, -1, -1, -1, -1, -1,
        -1, 1, 1, 1, -1, 1, 1,
        -1, 1, -1, 1, -1, 1, 1,
        -1, -1, -1, 1, -1, -1, -1,
        -1, -1, -1, -1, -1, 1, 1
    ]

    names = ["EUR", "USD", "GBP", "JPY", "AUD", "NZD", "CHF", "CAD"]

    class Meta:
        label = 'base'

        # text displayed at the top of --help output
        description = 'Spider Optic forex guider'

        # text displayed at the bottom of --help output
        epilog = 'Usage: spideroptic atr --timeframe 9'

        # controller level arguments. ex: 'spideroptic --version'
        arguments = [
            ### add a version banner
            ( [ '-v', '--version' ],
              { 'action'  : 'version',
                'version' : VERSION_BANNER } ),
        ]


    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()


    @ex(
        help='example atr',

        # sub-command level arguments. ex: 'spideroptic command1 --foo bar'
        arguments=[
            ### add a sample foo option under subcommand namespace
            ( [ '-t', '--timeframe' ],
              { 'help' : 'timeframe',
                'action'  : 'store',
                'dest' : 'timeframe' } ),
        ],
    )
    def atr(self):
        """Example sub-command."""

        data = {
            'timeframe' : 9,
        }

        ### do something with arguments
        if self.app.pargs.timeframe is not None:
            data['timeframe'] = self.app.pargs.timeframe

        data['assets'] = []

        for asset in self.symbols:
            candles = get_candles(period="D", instrument=asset, start=None, end=None)

            if len(candles) > 10:
                candles = prepare_cadles(candles)

                TR = 0
                prev = candles[-10]

                for candle in candles[-int(data['timeframe']):]:
                    TR += max([abs(candle.High - prev.Close),abs(candle.Low - prev.Close),candle.HL()])
                    prev = candle
                atr = TR/int(data['timeframe'])
                atr_percent = TR / int(data['timeframe']) / candles[-1].Close

                if atr_percent > 0.004:
                    data['assets'].append({'atr':atr,'asset':asset})

        self.app.render(data, 'atr.jinja2')

    @ex(
        help='example idx',
    )
    def idx(self):
        data = {}

        data['assets'] = {"EUR":100.0, "USD":100.0, "GBP":100.0, "JPY":100.0, "AUD":100.0, "NZD":100.0, "CHF":100.0, "CAD":100.0}
        contribution = 0.0
        index = 0
        for asset in self.symbols:
            candles = get_candles(period="D", instrument=asset, start=None, end=None)

            if len(candles) > 1:
                candles = prepare_cadles(candles)
                prev_candle = candles[-1]
                current_candle = candles[-2]
                contribution += (prev_candle.Close - current_candle.Close) / current_candle.Close * self.weights[index] / 7
            index += 1
            if  index % 7 == 0:
                data['assets'][self.names[int(index/7)-1]] = data['assets'][self.names[int(index/7)-1]] * (1 + contribution)

        x = np.linspace(0, 2 * np.pi, 100)
        y = [np.sin(m) + m for m in x]
        fig = apl.figure()
        fig.plot(x, y, width=60, height=20)
        fig.show()
        #self.app.render(data, 'idx.jinja2')
