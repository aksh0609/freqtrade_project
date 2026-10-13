# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement
# flake8: noqa: F401
# isort: skip_file
# --- Do not remove these libs ---
import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from typing import Optional, Union

from freqtrade.strategy import (
    IStrategy,
    Trade,
    Order,
    PairLocks,
    informative,
    DecimalParameter
)

# --------------------------------
# Add your lib to import here
try:
    import talib.abstract as ta
    from technical import qtpylib
except ImportError:
    # Fallback if talib is not available
    import freqtrade.vendor.qtpylib.indicators as qtpylib


class Manual_Control_Strategy(IStrategy):
    """
    Manual Control Strategy

    This is a completely manual trading strategy where YOU have full control.
    The bot will NOT make any automatic buy/sell decisions.

    How to use:
    1. Monitor the charts and indicators yourself
    2. Click "Force Entry" button in Web UI when you want to buy
    3. Click "Force Exit" button in Web UI when you want to sell

    The bot only provides useful indicators on the chart:
    - RSI (14)
    - MACD
    - Bollinger Bands
    - EMA 9, 21, 55
    - Volume

    You make ALL the trading decisions!
    """

    # Strategy interface version - allow new iterations of the strategy interface.
    INTERFACE_VERSION = 3

    # Optimal timeframe for the strategy.
    timeframe = '5m'

    # Can this strategy go short?
    can_short: bool = False

    # Minimal ROI designed for the strategy.
    # This will never trigger automatically since populate_entry_trend returns nothing
    minimal_roi = {
        "0": 0.10  # Exit at 10% profit (only if you manually enable it)
    }

    # Optimal stoploss designed for the strategy.
    # This protects your manually opened trades
    stoploss = -0.03  # -3% stop loss for safety

    # Trailing stoploss (optional protection)
    trailing_stop = True
    trailing_stop_positive = 0.01  # Lock in profit at 1%
    trailing_stop_positive_offset = 0.02  # Start trailing after 2% profit
    trailing_only_offset_is_reached = True

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = True

    # These values can be overridden in the config.
    use_exit_signal = False  # We don't use automatic exit signals
    exit_profit_only = False
    ignore_roi_if_entry_signal = True

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 200

    # Optional order type mapping.
    order_types = {
        'entry': 'limit',
        'exit': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'entry': 'GTC',
        'exit': 'GTC'
    }

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several technical indicators to help you make manual trading decisions.
        These will be visible on the charts in the Web UI.
        """

        # RSI - Relative Strength Index
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)

        # MACD - Moving Average Convergence Divergence
        macd = ta.MACD(dataframe)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']

        # Bollinger Bands
        bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(dataframe), window=20, stds=2)
        dataframe['bb_lowerband'] = bollinger['lower']
        dataframe['bb_middleband'] = bollinger['mid']
        dataframe['bb_upperband'] = bollinger['upper']
        dataframe['bb_percent'] = (dataframe['close'] - dataframe['bb_lowerband']) / (
            dataframe['bb_upperband'] - dataframe['bb_lowerband']
        )
        dataframe['bb_width'] = (dataframe['bb_upperband'] - dataframe['bb_lowerband']) / dataframe['bb_middleband']

        # EMA - Exponential Moving Averages
        dataframe['ema_9'] = ta.EMA(dataframe, timeperiod=9)
        dataframe['ema_21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema_55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema_200'] = ta.EMA(dataframe, timeperiod=200)

        # SMA - Simple Moving Averages
        dataframe['sma_20'] = ta.SMA(dataframe, timeperiod=20)
        dataframe['sma_50'] = ta.SMA(dataframe, timeperiod=50)

        # Stochastic RSI
        stoch_rsi = ta.STOCHRSI(dataframe)
        dataframe['stoch_rsi_k'] = stoch_rsi['fastk']
        dataframe['stoch_rsi_d'] = stoch_rsi['fastd']

        # Volume indicators
        dataframe['volume_mean_20'] = dataframe['volume'].rolling(window=20).mean()

        # ADX - Average Directional Index (trend strength)
        dataframe['adx'] = ta.ADX(dataframe)

        # ATR - Average True Range (volatility)
        dataframe['atr'] = ta.ATR(dataframe)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        NO AUTOMATIC ENTRIES!

        This strategy requires manual intervention.
        Use the "Force Entry" button in the Web UI to open trades.

        The bot will NEVER automatically enter trades.
        """
        dataframe.loc[:, 'enter_long'] = 0
        dataframe.loc[:, 'enter_tag'] = ''

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        NO AUTOMATIC EXITS!

        This strategy requires manual intervention.
        Use the "Force Exit" button in the Web UI to close trades.

        However, stoploss and trailing_stop will still protect your trades.
        """
        dataframe.loc[:, 'exit_long'] = 0
        dataframe.loc[:, 'exit_tag'] = ''

        return dataframe

    def custom_stoploss(self, pair: str, trade: Trade, current_time: datetime,
                       current_rate: float, current_profit: float, **kwargs) -> float:
        """
        Custom stoploss logic - you can modify this if needed.

        Default: -3% hard stop, then trailing stop kicks in at +2% profit
        """
        return self.stoploss

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                           time_in_force: str, current_time: datetime, entry_tag: Optional[str],
                           side: str, **kwargs) -> bool:
        """
        Allow all manual entries through Force Entry button.
        """
        return True

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                          rate: float, time_in_force: str, exit_reason: str,
                          current_time: datetime, **kwargs) -> bool:
        """
        Allow all manual exits and stop losses.
        """
        return True

    # Plot configuration - adds visual indicators to the chart
    plot_config = {
        'main_plot': {
            'ema_9': {'color': 'blue', 'width': 1},
            'ema_21': {'color': 'orange', 'width': 1},
            'ema_55': {'color': 'red', 'width': 1},
            'ema_200': {'color': 'purple', 'width': 2},
            'sma_20': {'color': 'green', 'width': 1},
            "bb_lowerband": {"color": "yellow", "width": 2},
            "bb_middleband": {"color": "cyan", "width": 2},
            "bb_upperband": {"color": "magenta", "width": 2},
        },
        'subplots': {
            "RSI": {
                'rsi': {'color': 'purple', 'width': 2},
            },
            "MACD": {
                'macd': {'color': 'blue', 'width': 1},
                'macdsignal': {'color': 'orange', 'width': 1},
            },
            "Stoch RSI": {
                'stoch_rsi_k': {'color': 'blue', 'width': 1},
                'stoch_rsi_d': {'color': 'orange', 'width': 1},
            },
        }
    }
