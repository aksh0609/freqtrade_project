import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import IStrategy, informative


class MichaelHarrisStrategy(IStrategy):
    """
    Michael Harris DAX Pattern Strategy
    Translated from 01_MichaelHarris_DAXPattern.ipynb

    This strategy uses a 7-point pattern recognition logic based on
    High/Low relationships of current and previous candles.
    """

    # Strategy interface version - keep it at 3
    INTERFACE_VERSION = 3

    # Optimal timeframe for this pattern on Crypto
    timeframe = "5m"

    # Startup period
    startup_candle_count = 200

    # Minimal ROI designed for the strategy.
    # Scalping-style ROI for 5m timeframe
    minimal_roi = {
        "0": 0.05,  # 5% at any time
        "15": 0.03,  # 3% after 15 mins
        "30": 0.015,  # 1.5% after 30 mins
        "60": 0.005,  # 0.5% after 1 hour (exit break-even or small gain)
    }

    # Optimal stoploss attempted until now
    stoploss = -0.03  # 3% stoploss for 5m chart

    # Trailing stoploss
    trailing_stop = True
    trailing_stop_positive = 0.005
    trailing_stop_positive_offset = 0.01
    trailing_only_offset_is_reached = True

    # Use entry signal as exit signal
    use_exit_signal = True
    exit_profit_only = False
    ignore_roi_if_entry_signal = False

    # Process only confirmed candles
    process_only_new_candles = True

    # Order type mapping
    order_types = {
        "entry": "market",
        "exit": "market",
        "stoploss": "market",
        "stoploss_on_exchange": False,
    }

    # Futures settings
    can_short = False

    @informative("1h")
    def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # 5m indicators
        dataframe["ema200"] = ta.EMA(dataframe, timeperiod=200)
        dataframe["adx"] = ta.ADX(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Populate entry signals with ADX and 1h Trend Filters
        """
        dataframe["enter_long"] = 0
        dataframe["enter_short"] = 0

        # --- TREND FILTERS ---
        # 5m Trend
        long_5m = dataframe["close"] > dataframe["ema200"]
        short_5m = dataframe["close"] < dataframe["ema200"]

        # 1h Trend (Big Picture)
        long_1h = dataframe["close"] > dataframe["ema200_1h"]
        short_1h = dataframe["close"] < dataframe["ema200_1h"]

        # Trend Strength (ADX > 25)
        trending = dataframe["adx"] > 25

        # --- PATTERN CONDITIONS ---
        # Long Pattern
        l1 = dataframe["high"] > dataframe["high"].shift(1)
        l2 = dataframe["high"].shift(1) > dataframe["low"]
        l3 = dataframe["low"] > dataframe["high"].shift(2)
        l4 = dataframe["high"].shift(2) > dataframe["low"].shift(1)

        # Short Pattern
        s1 = dataframe["low"] < dataframe["low"].shift(1)
        s2 = dataframe["low"].shift(1) < dataframe["high"]
        s3 = dataframe["high"] < dataframe["low"].shift(2)
        s4 = dataframe["low"].shift(2) < dataframe["high"].shift(1)

        # --- SIGNALS ---
        dataframe.loc[(long_5m & long_1h & trending & l1 & l2 & l3 & l4), "enter_long"] = 1

        dataframe.loc[(short_5m & short_1h & trending & s1 & s2 & s3 & s4), "enter_short"] = 1

        return dataframe

    def custom_stoploss(
        self, candle_date, trade, current_date, current_rate, current_profit, **kwargs
    ) -> float:
        """
        Breakeven logic: If profit reaches 1.2%, move SL to entry (0% loss)
        """
        if current_profit >= 0.012:
            return 0.001  # Small positive offset to cover fees

        return self.stoploss

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit signals - relying on ROI and Stoploss for now
        """
        dataframe.loc[:, "exit_long"] = 0
        dataframe.loc[:, "exit_short"] = 0

        return dataframe
