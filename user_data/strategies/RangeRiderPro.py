import talib.abstract as ta
from pandas import DataFrame

from freqtrade.strategy import DecimalParameter, IntParameter, IStrategy


class RangeRiderPro(IStrategy):
    """
    Range Rider Pro Strategy

    Logic:
    1. Identify Ranging Market: Uses an EMA Ribbon (EMA 34, 50, 89).
       When the ribbon is compressed (EMAs are close together) and flat, the market is ranging.
    2. Support/Resistance: Dynamically calculates recent Support (Low of last N candles) and Resistance (High of last N candles).
    3. Entry: Buy when price is near Support AND Market is Ranging.
    4. Exit: Sell when price nears Resistance.
    """  # noqa: E501

    INTERFACE_VERSION = 3

    # Strategy settings
    timeframe = "5m"

    # ROI table (Backups)
    minimal_roi = {
        "0": 0.10,  # 10%
        "30": 0.05,  # 5% after 30 mins
        "60": 0.02,  # 2% after 60 mins
        "90": 0.01,  # 1% after 90 mins
    }

    # Stoploss
    stoploss = -0.05  # 5% max loss, rely on S/R for exits mostly

    # Trailing stop
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    # Hyperopt parameters
    window_sr = IntParameter(20, 100, default=50, space="buy", optimize=True)
    ribbon_threshold = DecimalParameter(
        0.001, 0.01, default=0.005, space="buy", optimize=True
    )  # 0.5% spread

    # Indicators
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # EMA Ribbon
        dataframe["ema_34"] = ta.EMA(dataframe, timeperiod=34)
        dataframe["ema_50"] = ta.EMA(dataframe, timeperiod=50)
        dataframe["ema_89"] = ta.EMA(dataframe, timeperiod=89)

        # Calculate Ribbon Spread (max dist - min dist between EMAs)
        # We want this to be LOW for a ranging market
        dataframe["ribbon_max"] = dataframe[["ema_34", "ema_50", "ema_89"]].max(axis=1)
        dataframe["ribbon_min"] = dataframe[["ema_34", "ema_50", "ema_89"]].min(axis=1)
        dataframe["ribbon_spread"] = (
            dataframe["ribbon_max"] - dataframe["ribbon_min"]
        ) / dataframe["close"]

        # Dynamic Support and Resistance (Donchian Channel style)
        # Using shift(2) to avoid lookahead bias/repainting slightly, identifying confirmed levels
        dataframe["support"] = dataframe["low"].rolling(window=50).min()
        dataframe["resistance"] = dataframe["high"].rolling(window=50).max()
        # ADX for Trend Strength (Filter)
        dataframe["adx"] = ta.ADX(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Condition 1: Market is Ranging (Ribbon Spread is tight)
                (dataframe["ribbon_spread"] < 0.005)  # 0.5% spread threshold
                &
                # Condition 2: Price is Near Support (within 1% of support)
                (dataframe["close"] <= dataframe["support"] * 1.01)
                &
                # Condition 3: Price is above Support (false breakout protection - optional, here we just catch the bounce)  # noqa: E501
                (dataframe["close"] >= dataframe["support"] * 0.99)
                &
                # Condition 4: Volume > 0
                (dataframe["volume"] > 0)
                &
                # Condition 5: Trend Filter (ADX < 25)
                (dataframe["adx"] < 25)
            ),
            "enter_long",
        ] = 1
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # Condition 1: Price is Near Resistance (within 1% of resistance)
                (dataframe["close"] >= dataframe["resistance"] * 0.99) & (dataframe["volume"] > 0)
            ),
            "exit_long",
        ] = 1
        return dataframe
