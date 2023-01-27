from pathlib import Path

import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from matplotlib.animation import FuncAnimation, PillowWriter

# Functions
def add_geo_features(ax):
    """
    Add reference geographical layers such as thenational boundaries
    and the main lakes and rivers.
    """
    ax.add_feature(
        cfeature.NaturalEarthFeature(
            "cultural",
            "admin_0_boundary_lines_land",
            scale="10m",
            edgecolor="black",
            facecolor="none",
            linewidth=1,
        )
    )
    ax.add_feature(
        cfeature.NaturalEarthFeature(
            "physical",
            "rivers_lake_centerlines",
            scale="10m",
            edgecolor=np.array([0.59375, 0.71484375, 0.8828125]),
            facecolor="none",
            linewidth=1,
        )
    )

# Settings
## Paths
folder_rain = (r"Q:\Projekte\1000-\1200-\1296\1296.25 Netzbewirtschaftung "
    r"Worblental\05 Berechnungen Grundlagen\09 Regendaten")
folder_rain = Path(folder_rain)

path_raindata = (r"Q:\Projekte\1000-\1200-\1296\1296.25 Netzbewirtschaftung "
    r"Worblental\05 Berechnungen Grundlagen\09 Regendaten\MeteoSchweiz"
    r"\Daten\RR_INCA_202210240900.nc")

## Globals
epsg_lv03 = 21781
crs = ccrs.epsg(epsg_lv03)
dt_format = '%d.%m.%Y %H:%M'
zollikofen_coords = (601500, 205500)

# Read rain data
ds = xr.open_dataset(path_raindata)

# Plot precipitation field
levels = np.logspace(-1, 2, 10, base=10)
cmap = "Blues"

fig = plt.figure()

precip_field = ds.RR.isel(time=0)
precip_field = precip_field.where(precip_field > 0)
dt0_str = ds.time.to_pandas()[0].strftime(dt_format)

g = precip_field.plot(
    transform=crs,
    subplot_kws=dict(projection=crs),
    levels=levels,
    cmap=cmap
    )
ax = g.axes
title = ax.title
add_geo_features(ax)
ax.scatter(*zollikofen_coords, s=9, c='r')
ax.text(zollikofen_coords[0]+1e3, zollikofen_coords[1]+3e3, 'Zollikofen')

def animate(t):
    data = ds.RR.isel(time=t)
    time = ds.time.to_pandas()[t] # time as Timestamp()
    dt_str = time.strftime(dt_format)
    data = data.where(data > 0).data.flatten()
    g.set_array(data)
    title.set_text(dt_str)
    return (g, title) # must be given as tuple

def init():
    data = precip_field.data.flatten()
    g.set_array(data)
    title.set_text(dt0_str)
    return (g, title) # must be given as tuple

ani = FuncAnimation(fig, animate, range(len(ds.time)), init_func=init)

save_path = folder_rain / 'rain_animation.gif'
ani.save(save_path, writer=PillowWriter(fps=4))
