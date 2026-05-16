"""
aqi_colors.py

EPA Air Quality Index (AQI) colors and breakpoints for criteria pollutants.

AQI colors are taken directly from EPA specifications:
https://www.airnow.gov/aqi/aqi-basics/

Breakpoints follow EPA NAAQS standards:
- PM2.5: 24-hour standard
- O3: 8-hour 2015 standard
- NO2: 1-hour standard
"""

from matplotlib.patches import Rectangle

# EPA AQI colors (official hex values)
AQI_COLORS = {
    "green"  : "#00e400",
    "yellow" : "#ffff00",
    "orange" : "#ff7e00",
    "red"    : "#ff0000",
    "purple" : "#8f3f97",
    "maroon" : "#7e0023",
}

# PM2.5 breakpoints updated May 6, 2024
# Source: EPA Technical Assistance Document for AQI Reporting
# https://document.airnow.gov/technical-assistance-document-for-the-reporting-of-daily-air-quailty.pdf


# AQI breakpoints by pollutant
# Each entry: (low, high, color_name)
# high=None means "up to y_max" in plots
AQI_BREAKPOINTS = {
    "pm25": [
        (0.0,   12.0,  "green"),
        (12.1,  35.4,  "yellow"),
        (35.5,  55.4,  "orange"),
        (55.5,  150.4, "red"),
        (150.5, 250.4, "purple"),
        (250.5, None,  "maroon"),
    ],
    "o3_8hr": [
        (0.000, 0.054, "green"),
        (0.055, 0.070, "yellow"),
        (0.071, 0.085, "orange"),
        (0.086, 0.105, "red"),
        (0.106, 0.200, "purple"),
        (0.201, None,  "maroon"),
    ],
    "o3_1hr": [
        (0.000, 0.124, "green"),
        (0.125, 0.164, "yellow"),
        (0.165, 0.204, "orange"),
        (0.205, 0.404, "red"),
        (0.405, 0.504, "purple"),
        (0.505, None,  "maroon"),
    ],
    "no2": [
        (0,    53,   "green"),
        (54,   100,  "yellow"),
        (101,  360,  "orange"),
        (361,  649,  "red"),
        (650,  1249, "purple"),
        (1250, None, "maroon"),
    ],
}


def aqi_boxes(pollutant, start_dt, end_dt, y_max, alpha=0.2):
    """
    Generate matplotlib Rectangle patches with AQI color bands for a pollutant.

    Parameters
    ----------
    pollutant : str
        Pollutant key: "pm25", "o3_8hr", "o3_1hr", or "no2"
    start_dt : datetime
        Left edge of the plot time axis.
    end_dt : datetime
        Right edge of the plot time axis.
    y_max : float
        Upper limit of the plot y axis. Used for the open-ended top band.
    alpha : float, default 0.2
        Transparency of the color bands. Lower values give more pastel appearance.
        EPA official colors are used; alpha controls how they blend with the
        white plot background to produce a softer pastel effect.

    Returns
    -------
    list of matplotlib.patches.Rectangle

    Examples
    --------
    >>> for box in aqi_boxes("o3_8hr", start_dt, end_dt, o3_max):
    ...     ax.add_patch(box)
    """
    if pollutant not in AQI_BREAKPOINTS:
        raise ValueError(
            f"Unknown pollutant '{pollutant}'. "
            f"Choose from: {list(AQI_BREAKPOINTS.keys())}"
        )

    boxes = []
    width = end_dt - start_dt

    for lo, hi, color_name in AQI_BREAKPOINTS[pollutant]:
        hi_val = hi if hi is not None else y_max
        height = hi_val - lo
        boxes.append(Rectangle(
            (start_dt, lo),
            width,
            height,
            facecolor=AQI_COLORS[color_name],
            alpha=alpha,
        ))

    return boxes