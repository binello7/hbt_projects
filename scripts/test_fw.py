from pathlib import Path

import pandas as pd

from hbt import fremdwasser as fw

# Paths
data_dir = Path(r"C:\Users\sru\OneDrive - Hunziker Betatech AG"
    r"\Documents\04_Entwicklung\data\01_Rohdaten")
save_dir = Path(r"C:\Users\sru\Downloads\hist")
path_ara = data_dir / "Zulaufmenge_ARA_Skript_1min.csv"

# Read data
date_parser = lambda x: pd.to_datetime(x, format='%d.%m.%Y %H:%M:%S')
ts_ara = pd.read_csv(path_ara, sep=';', index_col=0, parse_dates=[0],
    date_parser=date_parser)

# Filter data
ts_ara = ts_ara[(ts_ara>=20) & (ts_ara<=150)]

fig = fw.hist_flow(ts_ara=ts_ara, save_dir=save_dir)
