from pandas import DataFrame
import talib.abstract as ta
from freqtrade.strategy import IStrategy


class BollingerBounceFearTrader(IStrategy):
    """
    Bollinger Bounce Fear Trader
    Strategy to buy panic (fear) and sell relief (greed).

    Logic:
    1. Buy when price < Lower BB AND RSI < 30 AND Volume > 1.5x Avg Volume.
    2. Sell when price > Middle BB (Mean Reversion).
    """

    INTERFACE_VERSION = 3

    # Long only
    can_short = False

    # ROI table: Backups in case mean reversion takes too long
    minimal_roi = {
        "0": 0.05,  # 5% profit target
        "20": 0.02,  # 2% profit after 20 mins
        "40": 0.01,  # 1% profit after 40 mins
        "60": 0.005,  # Exit break-even after 1 hour
    }

    # Stoploss: Tight protection against market crashes
    stoploss = -0.03  # 3% max loss

    # Timeframe
    timeframe = "5m"

    # Startup period for indicators
    startup_candle_count = 30

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Bollinger Bands (2.0 std dev)
        bollinger = ta.BBANDS(dataframe, timeperiod=20, nbdevup=2.0, nbdevdn=2.0, matype=0)
        dataframe["bb_upperband"] = bollinger["upperband"]
        dataframe["bb_middleband"] = bollinger["middleband"]
        dataframe["bb_lowerband"] = bollinger["lowerband"]

        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # Volume Moving Average (for detecting spikes)
        dataframe["volume_mean"] = dataframe["volume"].rolling(window=20).mean()

        # ADX for Trend Strength (Filter)
        dataframe["adx"] = ta.ADX(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # PRICE CRASH: Close below Lower Band
                (dataframe["close"] < dataframe["bb_lowerband"])
                &
                # OVERSOLD: RSI < 30
                (dataframe["rsi"] < 30)
                &
                # PANIC SELLING: Volume > 1.5x Average
                (dataframe["volume"] > (dataframe["volume_mean"] * 1.5))
                &
                # TREND FILTER: ADX < 25 (Avoid catching falling knives in strong trends)
                (dataframe["adx"] < 25)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[
            (
                # PROFIT TARGET: Price touches Middle Band (Mean Reversion)
                dataframe["close"] >= dataframe["bb_middleband"]
            ),
            "exit_long",
        ] = 1

        return dataframe
