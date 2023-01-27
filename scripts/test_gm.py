from hbt.utils_hbt import gm
from pathlib import Path
import pandas as pd

# Paths
path_ara = Path(r"Q:\Projekte\8000-\8400er\8431 ARA Sihltal\8431.15 Fremdwasser"
    r"\05 Berechnungen Grundlagen\Theoretische Auswertungen"
    r"\Datenauswertung R_sru\02_Bereinigte_Daten\Zulauf_ARA")
path_pop = Path(r"Q:\Projekte\8000-\8400er\8431 ARA Sihltal\8431.15 Fremdwasser"
    r"\05 Berechnungen Grundlagen\Theoretische Auswertungen"
    r"\Datenauswertung R_sru\02_Bereinigte_Daten\Einwohner\Einwohner.csv")
save_path = Path(r"Q:\Projekte\8000-\8400er\8431 ARA Sihltal"
    r"\8431.15 Fremdwasser\05 Berechnungen Grundlagen\Theoretische Auswertungen"
    r"\Datenauswertung R_sru\03_Auswertung\Python")

# Read ARA
path_files = path_ara.glob('*.csv')
ts_ara_d = pd.DataFrame()
date_parser = lambda x: pd.to_datetime(x, format='%d.%m.%Y')
for file in path_files:
    df = pd.read_csv(file, sep=';', header=None, index_col=0, parse_dates=[0], 
        date_parser=date_parser)
    ts_ara_d = pd.concat((ts_ara_d, df), axis=0)

# Read EW
date_parser = lambda x: pd.to_datetime(x, format='%Y')
ts_ew = pd.read_csv(path_pop, index_col=0, header=0, sep=';', parse_dates=[0],
    date_parser=date_parser)

spec_twv = 162
fw_y, fw_m = gm(ts_ara_d=ts_ara_d, ts_ew=ts_ew, spec_twv=spec_twv)

file_name = 'GM_Jahr.csv'
fw_y.to_csv((save_path / file_name), sep=';')
print(fw_y)

file_name = 'GM_Monat.csv'
fw_m.to_csv((save_path / file_name), sep=';')
print(fw_m)
