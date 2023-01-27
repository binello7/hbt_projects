from pathlib import Path

import pandas as pd

from hbt import fremdwasser as fw

data_dir = Path(r"C:\Users\ALFA\Downloads\01_Rohdaten")

path_ara = data_dir / "Zulaufmenge_ARA_Skript_1min.csv"
path_rain = data_dir / "data_1d.csv"
path_twv = data_dir / "Trinkwasserverbrauch_Monat.csv"

# Create ts_ara_d in m3/day
date_parser = lambda x: pd.to_datetime(x, format='%d.%m.%Y %H:%M:%S')
ts_ara = pd.read_csv(path_ara, sep=';', index_col=0, parse_dates=[0],
    date_parser=date_parser)
ts_ara_d = ts_ara.groupby(pd.Grouper(freq='D')).sum()
ts_ara_d = ts_ara_d * 60 / 1e3

date_parser = lambda x: pd.to_datetime(x, format='%d.%m.%Y')
ts_rain_d = pd.read_csv(path_rain, sep=';', index_col=0, parse_dates=[0],
    date_parser=date_parser)

# Create ts_twv_m in m3/month
date_parser = lambda x: pd.to_datetime(x, format='%m.%Y')
ts_twv_m = pd.read_csv(path_twv, sep=';', index_col=0, parse_dates=[0],
    date_parser=date_parser)

# Create ts_twv_y in m3/year
ts_twv_y = ts_twv_m.groupby(pd.Grouper(freq='Y')).sum()
ts_ew_y = ts_twv_y * 1e3 / 140 / 365

ts_y, ts_m = fw.jsm(ts_ara_d, ts_rain_d, ts_twv=ts_twv_m, freq_twv='month')

print(ts_y)
print(ts_m)
