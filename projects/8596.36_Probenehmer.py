from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import hbt.utils_hbt as uh
import matplotlib.dates as mdates

# Read data
path_pn = Path(r"Q:\Projekte\8000-\8500er\8596\8596.36-Mühlestrasse"
    r"\05 Berechnungen Grundlagen\Probenehmer\Envilab"
    r"\20220913_SABA Mühlestrasse_Zusammenstellung.xlsx")
path_rain = Path(r"Q:\Projekte\8000-\8500er\8596\8596.36-Mühlestrasse"
    r"\05 Berechnungen Grundlagen\Regendaten\Buchrain_1d.csv")

## Probenehmer
dt_format = '%d.%m.%Y %H:%M:%S'
date_parser = lambda x: pd.to_datetime(x, dayfirst=True, format=dt_format)
df_pn = pd.read_excel(path_pn, header=[0,1], parse_dates=[2,3,10,11],
    date_parser=date_parser)
dt_first = df_pn['IN']['von'].min()
dt_last = df_pn['IN']['von'].max()

## Rain
ts_rain = uh.read_raindata_agrometeo(file_path=path_rain, resolution='day')
ts_rain = ts_rain[(ts_rain.index >= dt_first) & (ts_rain.index <= dt_last)]
ts_rain = ts_rain.cumsum()
#-------------------------------------------------------------------------------

# # Plot 'Konzentration' - Linie
# compounds = ['GUS [mg/l]', 'Cu ges [mg/l]', 'Zn ges [mg/l]']
# basins = ['RFB 1', 'RFB 2', 'Ablauf Absetzbecken']
# n = len(compounds)
# fig, axs = plt.subplots(n)

# for i, c in enumerate(compounds):
#     for b in basins:
#         if b != 'Ablauf Absetzbecken':
#             df_temp = df_pn[df_pn['OUT']['Messstelle']==b]
#             axs[i].plot(df_temp['OUT']['von'], df_temp['OUT'][c], marker='o')
#         else:
#             df_temp = df_pn['IN'].drop_duplicates()
#             axs[i].plot(df_temp['von'], df_temp[c], marker='o')            
#     axs[i].legend(['RFB 1 (Splittfilter)', 'RFB 2 (Sandfilter)',
#         'Ablauf Absetzbecken'])
#     axs[i].set_ylabel('Konzentration [mg/l]')
#     axs[i].set_xlabel('Datum')
#     axs[i].set_title(c.replace(' [mg/l]', ''))
#     axs[i].grid(visible=True, axis='y')

# fig.set_size_inches(15,15)
# fig.set_dpi(300)
# path_save = Path(r"Q:\Projekte\8000-\8500er\8596\8596.36-Mühlestrasse"
#     r"\05 Berechnungen Grundlagen\Probenehmer\Auswertung_Konzentration_Linie")
# fig.savefig(path_save)
# #-------------------------------------------------------------------------------

# Plot 'Konzentration' - Balken / Text
compounds = ['GUS [mg/l]', 'Cu ges [mg/l]', 'Zn ges [mg/l]']
basins = ['RFB 1', 'RFB 2']
n = len(compounds)
data = df_pn['OUT']
dates1 = data[data['Messstelle']=='RFB 1'][['von', 'Messstelle']]
dates1.reset_index(drop=True, inplace=True)
dates2 = data[data['Messstelle']=='RFB 2'][['von', 'Messstelle']]
dates2.reset_index(drop=True, inplace=True)
# embed()

fig, axs = plt.subplots(n)
for i, c in enumerate(compounds):
    axs[i].bar(dates1.index - 0.2, data[data['Messstelle']=='RFB 1'][c],
        width=0.4)
    axs[i].bar(dates2.index + 0.2, data[data['Messstelle']=='RFB 2'][c],
        width=0.4)

    axs[i].set_xticks(dates1.index)
    axs[i].set_xticklabels(dates1['von'].apply(lambda x: x.strftime(
        '%d.%m.%y')))
fig.set_size_inches(15,15)
fig.set_dpi(300)

path_save = Path(r"Q:\Projekte\8000-\8500er\8596\8596.36-Mühlestrasse"
    r"\05 Berechnungen Grundlagen\Probenehmer"
    r"\Auswertung_Konzentration_Balken_text")
fig.savefig(path_save)
#-------------------------------------------------------------------------------

# Plot 'Konzentration' - Balken / Datum
compounds = ['GUS [mg/l]', 'Cu ges [mg/l]', 'Zn ges [mg/l]']
basins = ['RFB 1', 'RFB 2']
n = len(compounds)
data = df_pn['OUT']
rfb1 = data[data['Messstelle']=='RFB 1']
rfb1.set_index('von', inplace=True)
rfb2 = data[data['Messstelle']=='RFB 2']
rfb2.set_index('von', inplace=True)

fig, axs = plt.subplots(n)
width = 3
alpha = 0.6
leg1 = ['RFB 1 (Splittfilter)', 'RFB 2 (Sandfilter)']
leg2 = ['Regen']
for i, c in enumerate(compounds):
    axs[i].bar(rfb1.index, rfb1[c], width=width, color='r', alpha=alpha)
    axs[i].bar(rfb2.index, rfb2[c], width=width, color='g', alpha=alpha)
    ax2 = axs[i].twinx()
    ax2.plot(ts_rain.index, ts_rain.iloc[:,0], 'b-', alpha=0.5)
    axs[i].set_xlabel('Datum')
    axs[i].set_ylabel('Konzentration [mg/l]')
    ax2.set_ylabel('Regen kumulativ [mm]')
    axs[i].legend(leg1, loc=0)
    ax2.legend(leg2, loc=1)
    axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%m.%Y'))

fig.set_size_inches(15,15)
fig.set_dpi(300)
path_save = Path(r"Q:\Projekte\8000-\8500er\8596\8596.36-Mühlestrasse"
    r"\05 Berechnungen Grundlagen\Probenehmer"
    r"\Auswertung_Konzentration_Balken_datum")
fig.savefig(path_save)
#-------------------------------------------------------------------------------

# # Plot 'Wirkungsgrad'
# compounds = ['GUS [%]', 'Cu ges [%]', 'Zn ges [%]']
# basins = ['RFB 1', 'RFB 2']
# n = len(compounds)
# fig, axs = plt.subplots(n)

# for i, c in enumerate(compounds):
#     df_temp1 = df_pn[df_pn['RES'][c]>0]
#     for b in basins:
#         df_temp2 = df_temp1[df_temp1['OUT']['Messstelle']==b]
#         axs[i].plot(df_temp2['IN']['von'], df_temp2['RES'][c], marker='o')
#     axs[i].legend(['RFB 1 (Splittfilter)', 'RFB 2 (Sandfilter)',
#         'Ablauf Absetzbecken'])
#     axs[i].set_ylabel('Wirkungsgrad [%]')
#     axs[i].set_xlabel('Datum')
#     axs[i].set_title(c.replace(' [%]', ''))
#     axs[i].grid(visible=True, axis='y')

# fig.set_size_inches(15,15)
# fig.set_dpi(300)
# path_save = Path(r"Q:\Projekte\8000-\8500er\8596\8596.36-Mühlestrasse"
#     r"\05 Berechnungen Grundlagen\Probenehmer\Auswertung_Reinigung")
# fig.savefig(path_save)
# #-------------------------------------------------------------------------------
