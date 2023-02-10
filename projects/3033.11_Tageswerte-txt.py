from calendar import monthrange
from pathlib import Path

import pandas as pd

data_dir = Path(r"\\hunzikerwater.ch\DFSHBT\Daten-Winterthur\Projekte\3000-"
                r"\3033\3033.11 GEP\05 Berechnungen Grundlagen\TP Fremdwasser"
                r"\Daten_Aute_Kopie\Textdateien der Monatslisten\Protokoll")

save_dir = Path(r"\\hunzikerwater.ch\DFSHBT\Daten-Winterthur\Projekte\3000-"
                r"\3033\3033.11 GEP\05 Berechnungen Grundlagen\TP Fremdwasser")

year = 2017
suffix = f"{year}_01.TXT"
files_list = list(data_dir.glob(f"*{suffix}"))

encoding = "ansi"
sep = "\s+"
skiprows = 15
date_format = "%d.%m.%Y"
date_parser = lambda x: pd.to_datetime(x, format=date_format)

col_date = 'Datum'
col_vals = 'Total [m3]'
df_out = pd.DataFrame(columns=[col_date, col_vals])
for file in files_list:
    name = file.name
    month = int(name.replace(suffix, ""))
    n_days = monthrange(year=year, month=month)[1]
    df_in = pd.read_table(file, header=None, sep=sep, encoding=encoding,
                       skiprows=skiprows, parse_dates=True,
                       date_parser=date_parser, nrows=n_days)
    df_in.drop(columns=[0, 2, 3, 5], inplace=True)
    df_in.rename(columns={df_in.columns[0]: col_date,
                          df_in.columns[1]: col_vals}, inplace=True)
    df_out = pd.concat((df_out, df_in), axis='index')

df_out.set_index(df_out.columns[0], inplace=True)
df_out.to_excel((save_dir / "Tageswerte.xlsx"))
