from datetime import datetime
from pandas import DataFrame
from freqtrade.strategy import IStrategy, IntParameter
from freqtrade.persistence import Trade
import talib.abstract as ta
from technical import qtpylib


class BollingerBands_Strategy(IStrategy):
    INTERFACE_VERSION = 3

    # Can this strategy go short?
    can_short: bool = False

    # ROI (Return on Investment) table - Take profit levels
    minimal_roi = {
        "0": 0.025,  # 2.5% profit target
    }

    # Stoploss - Maximum loss allowed
    stoploss = -0.015  # -1.5% stop loss

    # Trailing stoploss
    trailing_stop = True
    trailing_stop_positive = 0.005  # Start trailing after 0.5% profit
    trailing_stop_positive_offset = 0.01  # Trailing kicks in at 1% profit
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
    buy_rsi_threshold = IntParameter(25, 40, default=35, space="buy", optimize=True)
    sell_rsi_threshold = IntParameter(60, 75, default=70, space="sell", optimize=True)
    bb_period = IntParameter(15, 25, default=20, space="buy", optimize=True)

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
        "main_plot": {
            "bb_upperband": {"color": "magenta", "width": 2},
            "bb_middleband": {"color": "cyan", "width": 2},
            "bb_lowerband": {"color": "yellow", "width": 2},
        },
        "subplots": {
            "RSI": {
                "rsi": {"color": "orange", "width": 2},
            },
            "BB Width": {
                "bb_width": {"color": "purple", "width": 1},
            },
        },
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Calculate technical indicators
        """
        # RSI - Relative Strength Index
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(
            qtpylib.typical_price(dataframe), window=self.bb_period.value, stds=2
        )
        dataframe["bb_lowerband"] = bollinger["lower"]
        dataframe["bb_middleband"] = bollinger["mid"]
        dataframe["bb_upperband"] = bollinger["upper"]

        # BB width - indicates volatility
        dataframe["bb_width"] = (dataframe["bb_upperband"] - dataframe["bb_lowerband"]) / dataframe[
            "bb_middleband"
        ]

        # BB percent - where is price relative to bands
        dataframe["bb_percent"] = (dataframe["close"] - dataframe["bb_lowerband"]) / (
            dataframe["bb_upperband"] - dataframe["bb_lowerband"]
        )

        # EMA 200 for Trend Filter
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Long only if price is above EMA 200
        dataframe.loc[
            (
                # Trend Filter
                (dataframe["close"] > dataframe["ema200"])
                &
                # Price is at or below the lower Bollinger Band
                (dataframe["close"] <= dataframe["bb_lowerband"])
                &
                # RSI confirms oversold
                (dataframe["rsi"] < self.buy_rsi_threshold.value)
                &
                # BB bands are not too tight (avoid low volatility periods)
                (dataframe["bb_width"] > 0.02)
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "enter_long",
        ] = 1

        # Short only if price is below EMA 200
        dataframe.loc[
            (
                # Trend Filter
                (dataframe["close"] < dataframe["ema200"])
                &
                # Short: Price is at or above the upper Bollinger Band
                (dataframe["close"] >= dataframe["bb_upperband"])
                &
                # RSI confirms overbought
                (dataframe["rsi"] > self.sell_rsi_threshold.value)
                &
                # BB bands are not too tight
                (dataframe["bb_width"] > 0.02)
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "enter_short",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                (
                    # Price reached middle band (mean reversion complete)
                    (dataframe["close"] >= dataframe["bb_middleband"])
                    |
                    # Or RSI is overbought
                    (dataframe["rsi"] > self.sell_rsi_threshold.value)
                )
                &
                # Volume check
                (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1

        dataframe.loc[
            (
                (
                    # Price reached middle band (mean reversion complete)
                    (dataframe["close"] <= dataframe["bb_middleband"])
                    |
                    # Or RSI is oversold
                    (dataframe["rsi"] < self.buy_rsi_threshold.value)
                )
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
        DCA logic for Bollinger Bands
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
