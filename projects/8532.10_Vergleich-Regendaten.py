from datetime import datetime as dt
from pathlib import Path

import hbt_tools.utils_hbt as uh
import pandas as pd

# Settings
path_raindata = Path(r"Q:\Projekte\8000-\8500er\8532\8532.10 GEP Richterswil"
    r"\05 Berechnungen Grundlagen\8 Entwässerungskonzept\MU Modell"
    r"\03_Regendaten\Wädenswil-Daten_2013-2018.csv")

dt_start = dt(2014, 7, 28, 16, 30)
dt_end = dt(2014, 7, 28, 22, 10)

df = uh.read_raindata_meteoschweiz(path_raindata, abbr=False)

mask = (df.index >= dt_start) & (df.index < dt_end)
df = df.iloc[mask]

# Save file
save_path = path_raindata.parent / 'waedenswil_regen-2014.csv'
df.to_csv(save_path)
