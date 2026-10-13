from datetime import datetime
from pandas import DataFrame
from freqtrade.strategy import IStrategy


class DipDetectionStrategy(IStrategy):
    """
    Strategy to catch sudden price spikes/dips.
    Places resting limit orders deep below the current market price.
    """

    INTERFACE_VERSION = 3

    can_short = False  # Dip catching is usually long-only

    # ROI: Exit quickly after the bounce
    minimal_roi = {
        "0": 0.03,  # 3% profit target
    }

    stoploss = -0.15  # Wide stop loss to allow for volatility

    timeframe = "5m"
    process_only_new_candles = True
    startup_candle_count = 20

    # Custom entry price logic
    def custom_entry_price(
        self,
        pair: str,
        current_time: datetime,
        proposed_rate: float,
        entry_tag: str,
        side: str,
        **kwargs,
    ) -> float:
        # Place the order 7% below the current market price
        return proposed_rate * 0.93

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # We don't need many indicators, just want the bot to always be "hunting"
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        # Always signal a buy for whitelisted pairs
        # The custom_entry_price will handle the "where"
        dataframe.loc[:, "enter_long"] = 1
        dataframe.loc[:, "enter_tag"] = "dip_hunt"
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe.loc[:, "exit_long"] = 0
        return dataframe
