from datetime import datetime as dt
from pathlib import Path

import plotly.graph_objects as go
from hbt_tools import utils as ut
from hbt_tools import utils_hbt as uh

# TODO
# 1. Add missing measurement units

# Globals
dt_format = '%d.%m.%Y %H:%M'
EZG_tot = 5.18 # ha

# Settings
# Installation: 21.04.2022 10:00
# Demontierung: 29.08.2022
dt_start = dt.strptime('21.04.2022 12:00', dt_format)
dt_end = dt.strptime('29.08.2022 00:00', dt_format)
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
        'yaxis': 'y3'
        },

    920: {
        'name': 'Niveau RFB1',
        'units': 'm',
        'yaxis': 'y3'
    },

    921: {
        'name': 'Niveau RFB2',
        'units': 'm',
        'yaxis': 'y3'
    },

}

# Y-axis
y_axes = {
    'yaxis': {
        'title': 'Durchfluss [l/s]',
        'color': 'black',
        'anchor': 'free',
        'side': 'left',
        'position': 0.0
    },
    # 'yaxis2': {
    #     'title': 'Niederschlag [mm]',
    #     'color': 'black',
    #     'anchor': 'free',
    #     'side': 'left',
    #     'position': 0.1
    # },
    'yaxis3': {
        'title': 'Niveau [m]',
        'color': 'black',
        'anchor': 'free',
        'side': 'left',
        'position': 0.2
    }
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

# Rain data
## Read rain data
ts_rain = uh.read_raindata_agrometeo(path_raindata, resolution='10min')

## Keep only data for the chosen period
ts_rain = ts_rain[(ts_rain.index>=dt_start) &
    (ts_rain.index<=dt_end)]

## Compute cumulative data
rain_cumsum = ts_rain.cumsum()
#-------------------------------------------------------------------------------

# Plot the data
## Plot measurements
fig = go.Figure()
for id, data in raw_data.items():
    x = data.index
    y = data['wert']
    name = measurements_units.loc[id]['name']
    yaxis = measurements_units.loc[id]['yaxis']

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        name=name,
        yaxis=yaxis
    ))

# ## Plot rain data
# fig.add_trace(go.Scatter(
#     x=ts_rain.index,
#     y=ts_rain.iloc[:,0],
#     name='Niederschlag',
#     yaxis='y2'
# ))

## Create axis objects
layout_kwargs = {'title': 'SABA Anschluss Baar',
                 'xaxis': {'domain': [0.2, 1.0]}}

for i, (y_ax, properties) in enumerate(y_axes.items()):
    layout_kwargs[y_ax] = {
        'title': properties['title'],
        'side': properties['side'],
        'titlefont': {
            'color': properties['color']
        },
        'anchor': properties['anchor'],
        'position': properties['position'],
        'tickfont': {
            'color': properties['color']
        }
    }

    if i > 0:
        layout_kwargs[y_ax] ['overlaying'] = 'y'

fig.update_layout(layout_kwargs)

## Save plot
date_str = ut.date_today_to_str()
save_path = save_path / (date_str + '_SABA-Baar.html')
fig.write_html(save_path)
