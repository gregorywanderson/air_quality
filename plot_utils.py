"""
plot_utils.py

Shared plotting helpers for the environmental-data notebooks.

Currently provides:
  * plot_hourly_heatmap  -- time-of-day vs day-of-year heatmap for hourly data
                            (continuous colormap or EPA AQI categorical).
  * nighttime_boxes      -- shaded Rectangle patches for nighttime periods,
                            for any location and timezone.
"""

import datetime as dt

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle
import pandas as pd
from suntime import Sun

from aqi_colors import AQI_COLORS, AQI_BREAKPOINTS


def plot_hourly_heatmap(
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
        and a column of numeric values to plot. Expects hourly (or coarser)
        data: the grid is 24 hours x days-of-year, one cell per (hour, day),
        so sub-hourly input overwrites cells and keeps only the last sample.
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
    plot_hourly_heatmap(o3_hourly, "datetime_local", "sample_measurement",
                      title="Hourly Ozone - Evanston Water Plant 2020",
                      colorbar_label="O3 (ppm)",
                      aqi_pollutant="o3_8hr")

    # Temperature with continuous colormap
    plot_hourly_heatmap(temp_data, "datetime_local", "sample_measurement",
                      title="Hourly Temperature - Evanston 2020",
                      colorbar_label="Temperature (C)",
                      cmap="RdBu_r",
                      vmin=-20, vmax=40)
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 5))

    # Guard: this plot assumes hourly (or coarser) data. Sub-hourly input
    # silently overwrites (hour, day) cells, so refuse it with a clear message.
    _times = (data.index if hasattr(data.index, "day_of_year")
              else pd.to_datetime(data[datetime_col]))
    _dt_min = pd.Series(_times).sort_values().diff().median()
    if pd.notna(_dt_min) and _dt_min < pd.Timedelta(minutes=50):
        raise ValueError(
            f"plot_hourly_heatmap expects hourly data; median timestep is "
            f"{_dt_min}. Resample to hourly before calling."
        )

    # Derive year from the data to handle leap years correctly
    if hasattr(data.index, 'year'):
        _year = data.index.year[0]
    elif datetime_col is not None:
        _year = pd.to_datetime(data[datetime_col]).iloc[0].year
    else:
        _year = pd.Timestamp.now().year
    n_days = 366 if pd.Timestamp(_year, 1, 1).is_leap_year else 365

    # Build 2D grid: rows=hours (0-23), cols=day of year (0-364)
    grid = np.full((24, n_days), np.nan)

    # Handle both DatetimeIndex and datetime column
    if hasattr(data.index, "day_of_year"):
        dt_series = data.index
    else:
        dt_series = pd.to_datetime(data[datetime_col])

    for _dt, row in zip(dt_series, data.itertuples()):
        doy = _dt.day_of_year - 1   # convert to 0-indexed
        hour = _dt.hour
        if 0 <= doy < n_days:
            grid[hour, doy] = getattr(row, value_col)

    # Build colormap - AQI categorical or continuous
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
        np.arange(grid.shape[1]), np.arange(grid.shape[0]), grid,
        cmap=colormap, norm=norm, alpha=alpha, shading='nearest'
    )

    # Month labels on x-axis
    month_starts = [
        pd.Timestamp(_year, month, 1).day_of_year - 1
        for month in range(1, 13)
    ]
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


def nighttime_boxes(
    start_datetime,
    end_datetime,
    y_max,
    latitude,
    longitude,
    timezone,
    alpha=0.30,
):
    """Return Rectangle patches covering nighttime periods.

    Parameters
    ----------
    start_datetime, end_datetime : datetime.datetime
        Window to shade, in local (naive) time matching the plot's x-axis.
    y_max : float
        Height of each shading rectangle (top of the axis).
    latitude, longitude : float
        Site coordinates, for sunrise/sunset computation.
    timezone : datetime.tzinfo
        Local timezone (e.g. pytz.timezone("America/Chicago")) used to convert
        suntime's UTC sunrise/sunset to the plot's local wall-clock time.
    alpha : float, default 0.30
        Shading opacity.

    Returns
    -------
    list of matplotlib.patches.Rectangle
    """
    solar_day = dt.timedelta(days=1)
    number_of_days = (end_datetime - start_datetime).days

    sun = Sun(latitude, longitude)

    sunrise = [None] * (number_of_days + 1)
    sunset = [None] * (number_of_days + 1)

    for day_number in range(number_of_days + 1):
        day = start_datetime + day_number * solar_day

        sunrise[day_number] = (
            sun.get_sunrise_time(day)
            .astimezone(timezone)
            .replace(tzinfo=None)
        )
        sunset[day_number] = (
            sun.get_sunset_time(day + solar_day)
            .astimezone(timezone)
            .replace(tzinfo=None)
        )

    boxes = [
        Rectangle(
            (start_datetime, 0),
            sunrise[0] - start_datetime,
            y_max,
            facecolor="dimgray",
            alpha=alpha,
        )
    ]

    for day_number in range(number_of_days):
        boxes.append(
            Rectangle(
                (sunset[day_number], 0),
                sunrise[day_number + 1] - sunset[day_number],
                y_max,
                facecolor="dimgray",
                alpha=alpha,
            )
        )

    return boxes
