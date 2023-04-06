from datetime import datetime as dt
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from hbt_tools import utils_hbt as uh
from matplotlib import rcParams

rcParams.update({'figure.autolayout': True})

# TODO
# 1. Add missing measurement units

# Globals
dt_format = '%d.%m.%Y %H:%M'
EZG_tot = 5.18 # ha

# Settings
# Installation: 21.04.2022 10:00
# Demontierung: 29.08.2022
dt_start = dt.strptime('07.06.2022 00:00', dt_format)
dt_end = dt.strptime('08.06.2022 00:00', dt_format)
if 'dt_end' not in vars():
    dt_end = dt.now()

## Paths
path_raindata = Path(r'Q:\Projekte\10000-\10208.10 Tangente Zug'
    r'\05 Berechnungen Grundlagen\Regendaten\Baar_data.csv')
path_watersamples = Path(r'Q:\Projekte\10000-\10208.10 Tangente Zug'
    r'\05 Berechnungen Grundlagen\Probenehmer\Wasserproben'
    r'\20220610_Wasserproben_SABA-Baar.xlsx')
path_wateranalysis = Path(r'Q:\Projekte\10000-\10208.10 Tangente Zug'
    r'\05 Berechnungen Grundlagen\Probenehmer\Auswertung_Wasserproben.csv')
save_path = Path(r"Q:\Projekte\10000-\10208.10 Tangente Zug"
    r"\05 Berechnungen Grundlagen\Datenauswertung\Plots")
#-------------------------------------------------------------------------------

# Measurements units
## Ablaufmenge Q2, Zulaufmenge Q1, Niveau ASB, Niveau RFB1, Niveau RFB2
measurements_units = {
    # 917: {
    #     'name': 'Durchfluss Q1',
    #     'units': 'l/s',
    #     'yaxis': 'y1'
    #     },

    # 918: {
    #     'name': 'Durchfluss Q2',
    #     'units': 'l/s',
    #     'yaxis': 'y1'
    #     },

    919: {
        'name': 'Niveau ASB',
        'units': 'm',
        },

    920: {
        'name': 'Niveau RFB1',
        'units': 'm',
    },

    921: {
        'name': 'Niveau RFB2',
        'units': 'm',
    },

}
#-------------------------------------------------------------------------------

# Get data from Messdatenbank
measurements_units = uh.measurements_to_df(measurements_units)
   
raw_data = {}
for id, row in measurements_units.iterrows():
    data = uh.hbtdb_get_data(hbt_id=id, dt_from=dt_start, dt_to=dt_end)

    raw_data.update({id: data})
    del data
#-------------------------------------------------------------------------------

# Plot the data
fig, ax = plt.subplots()
ax.plot(raw_data[920] * 100, 'b', label='RFB 1')
ax.plot(raw_data[921] * 100, 'r', label='RFB 2')

ax.tick_params(axis='x', labelrotation=30)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y %H:%M'))
ax.set_ylabel('Niveau [cm]')
fig.legend()

fig.savefig(save_path / 'alle_becken.png')
