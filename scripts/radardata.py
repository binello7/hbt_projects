from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import xarray as xr

from hbt_tools import export as ex


# Functions
def ts_from_xarray(ds, coords):
    '''
    Generates a timeseries from a xarray.Dataset at the specified coordinates.
    '''
    
    ts = ds.sel(chx=coords[0], chy=coords[1], method='nearest')
    ts_data = ts.RR
    ts_time = ts.time
    ts = pd.DataFrame(index=ts_time, data=ts_data)
    ts.index.name = 'timestamp'
    ts.rename(columns={0: 'rain [mm]'}, inplace=True)
    return ts

# Globals
coords_waedenswil = (693848, 230744)
coords_richterswil = (695642.2, 230031.4)

files_dir = Path(r"C:\Users\sru\Downloads\radardaten_2212")
save_dir = Path(r"C:\Users\sru\OneDrive - Hunziker Betatech AG\Documents"
    r"\04_Entwicklung\outputs")
save_path = save_dir / 'radar-observations_2212.nc'

files_list = list(files_dir.glob('*.nc'))
files_list.sort()

if False:
    ds = xr.open_dataset(save_path)

    ts_waedenswil = ts_from_xarray(ds, coords_waedenswil)
    ts_richterswil = ts_from_xarray(ds, coords_richterswil)

    fig, ax = plt.subplots()
    ax.plot(ts_waedenswil, label='Wädenswil')
    ax.plot(ts_richterswil, label='Richterswil')
    ax.legend()
    ax.set_xlabel('Datum')
    ax.set_ylabel('Niederschlag [mm]')

    fig.set_size_inches(20, 15)
    save_name = 'Niederschlag_Wädenswil-Richterswil.png'
    plt.savefig((save_dir / save_name))

    sum_waedenswil = ts_waedenswil.sum()
    sum_richterswil = ts_richterswil.sum()
    print(f"wädenswil: {sum_waedenswil}")
    print(f"richterswil: {sum_richterswil}")
