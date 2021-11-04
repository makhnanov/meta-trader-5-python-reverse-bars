import os
import time
import MetaTrader5 as mt5

from colorama import init
from colorama import Fore, Back
from prettytable import PrettyTable


init()


pairs = [
    "EURUSDrfd",
    "GBPUSDrfd",
    "USDJPYrfd",
    "USDCHFrfd",
    "USDCADrfd",
    "AUDUSDrfd",
    "NZDUSDrfd",
    "USDRUBrfd",
    "EURRUBrfd",
    "EURJPYrfd",
    "EURCADrfd",
    "EURCHFrfd",
    "EURNZDrfd",
    "GBPCADrfd",
    "USDSGDrfd",
    "USDZARrfd",
    "EURDKKrfd",
    "EURNOKrfd",
    "EURSEKrfd",
    "GBPAUDrfd",
    "GBPCHFrfd",
    "GBPJPYrfd",
    "USDDKKrfd",
    "USDMXNrfd",
    "USDNOKrfd",
    "USDSEKrfd",
    "CHFJPYrfd",
    "GBPNZDrfd",
    "AUDCADrfd",
    "AUDCHFrfd",
    "AUDJPYrfd",
    "AUDNZDrfd",
    "EURAUDrfd",
    "EURGBPrfd",

    # "XAUUSDrfd",
    # "XAGUSDrfd",
    # "USDHKDrfd",
    # "CADCHFrfd",
    # "CADJPYrfd",
    # "NZDCADrfd",
    # "NZDJPYrfd",
    # "EURSGDrfd",
    # "NZDCHFrfd",

    # "GBPSEKrfd",
]


O = 1
H = 2
L = 3
C = 4


def clear():
    os.system('cls')


# подключимся к MetaTrader 5
if not mt5.initialize():
    print("initialize() failed")
    mt5.shutdown()


def calculate_row_data(pair):
    t15 = detect_reverse_bar(mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_M15, 0, 1)[0], "15")
    t30 = detect_reverse_bar(mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_M30, 0, 1)[0], "30")
    th1 = detect_reverse_bar(mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_H1, 0, 1)[0], "H1")
    th4 = detect_reverse_bar(mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_H4, 0, 1)[0], "H4")
    td1 = detect_reverse_bar(mt5.copy_rates_from_pos(pair, mt5.TIMEFRAME_D1, 0, 1)[0], "D1")
    # if not t15 and not t30 and not th1 and not th4 and not td1:
    #     raise UserWarning
    try:
        return [
            pair,
            t15,
            t30,
            th1,
            th4,
            td1
        ]
    except TypeError:
        return [pair, "ERROR", "ERROR", "ERROR", "ERROR", "ERROR"]


def detect_reverse_bar(last_bar, period):
    price_open = last_bar[O]
    high = last_bar[H]
    low = last_bar[L]
    close = last_bar[C]

    part = (high - low) / 3

    bull_high = high
    bull_low = high - part
    bear_high = low + part
    bear_low = low

    if bear_high <= price_open <= bull_high and bull_low <= close <= bull_high:
        return Back.GREEN + Fore.BLACK + period + Fore.WHITE + Back.BLACK
    elif bear_low <= price_open <= bull_low and bear_low <= close <= bear_high:
        return Back.RED + Fore.BLACK + period + Fore.WHITE + Back.BLACK
    else:
        return ""


timeframes = ["15", "30", "H1", "H4", "D1"]


while True:
    table = PrettyTable()
    # table.border = False
    header = ["Pair"]
    header.extend(timeframes)
    table.field_names = header

    for pair in pairs:
        try:
            table.add_row(calculate_row_data(pair))
        except UserWarning:
            pass

    clear()

    print(table)
    time.sleep(1)
