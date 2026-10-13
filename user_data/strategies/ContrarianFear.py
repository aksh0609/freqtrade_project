from freqtrade.strategy import IStrategy, IntParameter, DecimalParameter
from pandas import DataFrame
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class ContrarianFear(IStrategy):
    """
    Contrarian Fear Buying Strategy

    Philosophy: "Be greedy when others are fearful."

    Mechanics:
    1. Wait for PANIC: RSI is extremely low (< 25) AND Price smashed below Lower Bollinger Band.
    2. Confirm PANIC: Volume spike (Panic Selling).
    3. ENTRY: Enter Long.
    4. EXIT: Mean reversion to the middle or upper Bollinger Band, or RSI recovery.
    """

    INTERFACE_VERSION = 3

    # Minimal ROI designed for the strategy.
    minimal_roi = {
        "0": 0.05,  # 5% profit immediately
        "30": 0.02,  # 2% profit after 30 mins
        "60": 0.01,  # 1% profit after 60 mins
        "120": 0,  # Break even after 2 hours
    }

    # Stoploss: Panic trades can be volatile. Give it room but protect against crashes.
    stoploss = -0.10  # 10% stoploss

    # Trailing stop: Once it goes up, lock in profits
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.02
    trailing_only_offset_is_reached = True

    # Optimal timeframe for the strategy
    timeframe = "5m"

    # Run "populate_indicators" on new candles only
    process_only_new_candles = True

    # Strategy parameters
    buy_rsi = IntParameter(10, 30, default=20, space="buy")
    sell_rsi = IntParameter(60, 90, default=70, space="sell")

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # RSI
        dataframe["rsi"] = ta.RSI(dataframe, timeperiod=14)

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe["bb_lowerband"] = bollinger["lower"]
        dataframe["bb_middleband"] = bollinger["mid"]
        dataframe["bb_upperband"] = bollinger["upper"]

        # Volume Weighted Average or simple Volume SMA
        dataframe["volume_mean"] = dataframe["volume"].rolling(window=20).mean()

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Entry Signal: Extreme Oversold Condition (Fear)
        """
        dataframe.loc[
            (
                (dataframe["rsi"] < self.buy_rsi.value)  # Extreme RSI Low (Fear)
                & (dataframe["close"] < dataframe["bb_lowerband"])  # Price below Lower BB
                & (
                    dataframe["volume"] > dataframe["volume_mean"] * 1.5
                )  # Volume Spike (Panic Selling)
            ),
            "enter_long",
        ] = 1

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Exit Signal: Recovery to Mean or Greed
        """
        dataframe.loc[
            (
                (dataframe["rsi"] > self.sell_rsi.value)  # Trend reversed to Greed
                | (dataframe["close"] > dataframe["bb_middleband"])  # Reverted to Mean
            ),
            "exit_long",
        ] = 1

        return dataframe
