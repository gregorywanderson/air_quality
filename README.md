# Air Quality Analysis

Jupyter notebooks and Python utilities for analyzing air quality data from the
[EPA Air Quality System (AQS)](https://www.epa.gov/aqs), the
[CROCUS](https://crocus-urban.org/) urban observatory network, and NEIU's
[QuantAQ MODULAIR](https://www.quantaq.com/modulair) low-cost sensor.

---

## Repository Structure

| File | Description |
|---|---|
| `aqs_ozone_timeseries.ipynb` | Time-series analysis of ozone readings from EPA AQS monitoring stations |
| `aqs_ozone_regional.ipynb` | Regional/spatial analysis of ozone data across multiple AQS sites |
| `modulair_examples.ipynb` | Working examples for pulling and visualizing data from the NEIU MODULAIR sensor |
| `aqs_utils.py` | Helper functions for ingesting and wrangling AQS API data (datetime parsing, validation) |
| `aqs_codes.py` | AQS parameter and method code constants |
| `aqi_colors.py` | AQI color scale mappings (Good → Hazardous) for consistent plot styling |
| `fips_codes.py` | FIPS geographic code lookups for state/county filtering |
| `plot_time_heatmap.py` | Time-of-day × day-of-week heatmap plot utility |

---

## Setup

### 1. Install dependencies

```bash
pip install pyaqsapi pandas numpy matplotlib cartopy suntime python-dotenv
```

> **Note:** `cartopy` may require system-level dependencies. See the
> [cartopy install docs](https://scitools.org.uk/cartopy/docs/latest/installing.html) if you run into issues.

### 2. Configure AQS API credentials

The AQS notebooks use [`pyaqsapi`](https://github.com/USEPA/pyaqsapi) to pull data from EPA's DataMart.
You'll need a free API key from EPA:

1. Register at [https://aqs.epa.gov/data/api/signup](https://aqs.epa.gov/data/api/signup)
2. Create a `.env` file in the project root:

```
AQS_USERNAME=your_email@example.com
AQS_KEY=your_api_key
```

The notebooks load credentials with `python-dotenv` — never commit your `.env` file.

### 3. Launch Jupyter

```bash
jupyter notebook
```

---

## Data Sources

**EPA AQS (Air Quality System)**
The primary source for regulatory-grade air quality measurements. Data is fetched via the
`pyaqsapi` library, which wraps EPA's public REST API. The `aqs_utils.py` module handles
datetime wrangling (local and GMT) and basic validation of API responses.

**CROCUS Network**
The Chicago Region Environmental and Climate Observing System — a network of urban sensors
focused on hyperlocal environmental monitoring across the Chicago metro area.

**QuantAQ MODULAIR (NEIU)**
A low-cost air quality sensor deployed at Northeastern Illinois University (NEIU),
measuring PM2.5, PM10, CO, NO, NO₂, and O₃. The `modulair_examples.ipynb` notebook
demonstrates how to access and visualize this data.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pyaqsapi` | EPA AQS DataMart API client |
| `pandas` / `numpy` | Data manipulation |
| `matplotlib` | Plotting |
| `cartopy` | Geospatial map projections |
| `suntime` | Sunrise/sunset times (for diurnal analysis) |
| `python-dotenv` | Loading API credentials from `.env` |
