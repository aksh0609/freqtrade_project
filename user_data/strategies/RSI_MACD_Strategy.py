from datetime import datetime
from pandas import DataFrame
from freqtrade.strategy import IStrategy, IntParameter
from freqtrade.persistence import Trade
import talib.abstract as ta
from technical import qtpylib


class RSI_MACD_Strategy(IStrategy):
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # ROI (Return on Investment) table - Take profit levels
    minimal_roi = {
        "0": 0.03,  # 3% profit target
    }

    # Stoploss - Maximum loss allowed
    stoploss = -0.02  # -2% stop loss

    # Trailing stoploss (moves the stoploss up as price goes up)
    trailing_stop = True
    trailing_stop_positive = 0.01  # Start trailing after 1% profit
    trailing_stop_positive_offset = 0.015  # Trailing kicks in at 1.5% profit
    trailing_only_offset_is_reached = True

    # Timeframe
    timeframe = "5m"

    # Run populate_indicators() only for new candle
    process_only_new_candles = True

    # These values can be overridden in the config
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Hyperoptable parameters (can be optimized)
    buy_rsi = IntParameter(20, 40, default=30, space="buy", optimize=True)
    sell_rsi = IntParameter(60, 80, default=70, space="sell", optimize=True)

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 30

    # Order types
    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Order time in force
    order_time_in_force = {"entry": "GTC", "exit": "GTC"}

    # Plot configuration for freqtrade-plot
    plot_config = {
        "main_plot": {},
        "subplots": {
            "RSI": {
                "rsi": {"color": "red"},
            },
            "MACD": {
                "macd": {"color": "blue"},
                "macdsignal": {"color": "orange"},
                "macdhist": {"color": "gray"},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate technical indicators
        """
        # RSI - Relative Strength Index
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # MACD - Moving Average Convergence Divergence
        macd = ta.MACD(dataframe, fastperiod=12, slowperiod=26, signalperiod=9)
        dataframe["macd"] = macd["macd"]
        dataframe["macdsignal"] = macd["macdsignal"]
        dataframe["macdhist"] = macd["macdhist"]

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry signal logic
        """
        dataframe.loc[
            (
                # RSI is oversold (price is low, might go up)
                (dataframe["rsi"] < self.buy_rsi.value)
                &
                # MACD crosses above signal line (bullish signal)
                (qtpylib.crossed_above(dataframe["macd"], dataframe["macdsignal"]))
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        dataframe.loc[
            (
                # RSI is overbought (price is high, might go down)
                (dataframe["rsi"] > self.sell_rsi.value)
                &
                # MACD crosses below signal line (bearish signal)
                (qtpylib.crossed_below(dataframe["macd"], dataframe["macdsignal"]))
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit signal logic
        """
        dataframe.loc[
            (
                # RSI is overbought (price is high, might go down)
                (dataframe["rsi"] > self.sell_rsi.value)
                &
                # MACD crosses below signal line (bearish signal)
                (qtpylib.crossed_below(dataframe["macd"], dataframe["macdsignal"]))
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1

        dataframe.loc[
            (
                # RSI is oversold
                (dataframe["rsi"] < self.buy_rsi.value)
                &
                # MACD crosses above signal line
                (qtpylib.crossed_above(dataframe["macd"], dataframe["macdsignal"]))
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "exit_short",
        ] = 1

        return dataframe

    def adjust_trade_position(
        self,
        trade: "Trade",
        current_time: "datetime",
        current_rate: float,
        current_profit: float,
        min_stake: float | None,
        max_stake: float,
        **kwargs,
    ) -> float | None:
        """
        DCA logic for RSI-MACD
        """
        if current_profit > -0.05:
            return None

        filled_entries = trade.select_filled_orders(trade.entry_side)
        count_of_entries = len(filled_entries)

        if count_of_entries <= 3:
            stake_amount = filled_entries[0].cost
            if (trade.stake_amount + stake_amount) <= max_stake:
                return stake_amount

        return None
