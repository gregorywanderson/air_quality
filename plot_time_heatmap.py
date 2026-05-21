"""
plot_time_heatmap.py

Time-of-day vs day-of-year heatmap for environmental timeseries data.

Useful for visualizing diurnal and seasonal patterns in hourly data such as
ozone, PM2.5, NO2, temperature, solar radiation, and other measurements.
Supports both EPA AQI categorical coloring and continuous colormaps.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
from aqi_colors import AQI_COLORS, AQI_BREAKPOINTS


def plot_time_heatmap(
    data,
    datetime_col,
    value_col,
    title=None,
    ylabel="Hour (local time)",
    colorbar_label=None,
    aqi_pollutant=None,
    cmap="YlOrRd",
    vmin=None,
    vmax=None,
    alpha=0.85,
    ax=None,
):
    """
    Plot a time-of-day vs day-of-year heatmap.

    Parameters
    ----------
    data : pd.DataFrame
        Must contain a datetime column or have a DatetimeIndex,
        and a column of numeric values to plot.
    datetime_col : str
        Name of the datetime column. Ignored if data has a DatetimeIndex.
    value_col : str
        Name of the column containing the values to plot.
    title : str, optional
        Plot title.
    ylabel : str, default "Hour (local time)"
        Y-axis label.
    colorbar_label : str, optional
        Label for the colorbar. Defaults to value_col if not provided.
    aqi_pollutant : str, optional
        If provided, colors snap to AQI breakpoints for this pollutant.
        Choose from: "o3_8hr", "o3_1hr", "pm25", "no2".
        If None, uses a continuous colormap.
    cmap : str, default "YlOrRd"
        Matplotlib colormap name. Used only when aqi_pollutant is None.
        Use "RdBu_r" for temperature.
    vmin : float, optional
        Minimum value for continuous colormap. Defaults to data minimum.
    vmax : float, optional
        Maximum value for continuous colormap. Defaults to data maximum.
    alpha : float, default 0.85
        Transparency of the heatmap cells. EPA AQI colors are used at full
        saturation; alpha blends them with the white background for a softer
        pastel appearance.
    ax : matplotlib.axes.Axes, optional
        Axes to plot on. Creates a new figure if None.

    Returns
    -------
    matplotlib.axes.Axes

    Examples
    --------
    # Ozone with AQI colors
    plot_time_heatmap(o3_hourly, "datetime_local", "sample_measurement",
                      title="Hourly Ozone — Evanston Water Plant 2020",
                      colorbar_label="O₃ (ppm)",
                      aqi_pollutant="o3_8hr")

    # Temperature with continuous colormap
    plot_time_heatmap(temp_data, "datetime_local", "sample_measurement",
                      title="Hourly Temperature — Evanston 2020",
                      colorbar_label="Temperature (°C)",
                      cmap="RdBu_r",
                      vmin=-20, vmax=40)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 5))

    # Build 2D grid: rows=hours (0-23), cols=day of year (0-364)
    n_days = 366 if pd.Timestamp(year, 1, 1).is_leap_year else 365
    grid = np.full((24, n_days), np.nan)

    # Handle both DatetimeIndex and datetime column
    if hasattr(data.index, "day_of_year"):
        dt_series = data.index
    else:
        dt_series = pd.to_datetime(data[datetime_col])

    for dt, row in zip(dt_series, data.itertuples()):
        doy = dt.day_of_year - 1   # convert to 0-indexed
        hour = dt.hour
        if 0 <= doy < 365:
            grid[hour, doy] = getattr(row, value_col)

    # Build colormap — AQI categorical or continuous
    if aqi_pollutant is not None:
        if aqi_pollutant not in AQI_BREAKPOINTS:
            raise ValueError(
                f"Unknown pollutant '{aqi_pollutant}'. "
                f"Choose from: {list(AQI_BREAKPOINTS.keys())}"
            )
        bounds = [bp[0] for bp in AQI_BREAKPOINTS[aqi_pollutant]]
        top = max(np.nanmax(grid) if np.any(~np.isnan(grid)) else 1.0,
            bounds[-1] + 0.001)
        last_hi = AQI_BREAKPOINTS[aqi_pollutant][-1][1]
        bounds.append(last_hi if last_hi is not None else top)
        colors = [AQI_COLORS[bp[2]] for bp in AQI_BREAKPOINTS[aqi_pollutant]]
        colormap = mcolors.ListedColormap(colors)
        norm = mcolors.BoundaryNorm(bounds, colormap.N)
    else:
        colormap = cmap
        norm = mcolors.Normalize(
            vmin=vmin if vmin is not None else np.nanmin(grid),
            vmax=vmax if vmax is not None else np.nanmax(grid),
        )

    # Plot the heatmap
    mesh = ax.pcolormesh(
        np.arange(365), np.arange(24), grid,
        cmap=colormap, norm=norm, alpha=alpha
    )

    # Month labels on x-axis
    month_starts = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ax.set_xticks(month_starts)
    ax.set_xticklabels(month_labels)

    # Hour labels on y-axis every 3 hours
    ax.set_yticks(range(0, 24, 3))
    ax.set_yticklabels([f"{h:02d}:00" for h in range(0, 24, 3)])
    ax.set_ylabel(ylabel)

    if title:
        ax.set_title(title)

    plt.colorbar(mesh, ax=ax, label=colorbar_label or value_col)

    return ax