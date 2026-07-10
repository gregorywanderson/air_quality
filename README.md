# Air Quality Analysis

Jupyter notebooks and Python utilities for analyzing air quality data from two
sources: the [EPA Air Quality System (AQS)](https://www.epa.gov/aqs), and a
rooftop pairing of a [QuantAQ MODULAIR](https://www.quantaq.com/modulair)
low-cost air-quality sensor with an Ambient Weather WS-500 station on the roof of
BBH on the main campus of Northeastern Illinois University (NEIU).

> **Note:** CROCUS urban-observatory work that previously lived here has moved to
> its own repository, [`crocus`](https://github.com/gregorywanderson/crocus).
> This repo now focuses on the EPA AQS and NEIU QuantAQ/WS-500 sources.

---

## Repository Structure

**Notebooks**

| Notebook | Description |
|---|---|
| `aqs_ozone_study_cook.ipynb` | Cook County ozone study: timeseries, calendar heatmaps, top-ozone-day event panels, and wind/pollutant roses (Northbrook lake-breeze diagnostic) |
| `aqs_ozone_timeseries.ipynb` | Time-series analysis of ozone readings from EPA AQS monitoring stations |
| `aqs_ozone_regional.ipynb` | Regional/spatial analysis of ozone across multiple AQS sites (uses `cartopy` maps) |
| `neiu_ozone_study.ipynb` | NEIU rooftop study pairing QuantAQ MODULAIR gases with Ambient Weather WS-500 wind: heatmaps, event panels, and roses |
| `modulair_examples.ipynb` | Working examples for pulling and visualizing NEIU MODULAIR data |
| `particulate_matter.ipynb` | Particulate-matter analysis |
| `habitatmapdownloader.ipynb` | Downloader for AirBeam / HabitatMap data (in progress) |

**Modules**

| Module | Description |
|---|---|
| `aqs_utils.py` | Ingest and wrangle AQS API data (datetime parsing, validation, downloads) |
| `aqs_codes.py` | AQS parameter and method code constants |
| `aqi_colors.py` | AQI color scale and breakpoints (Good → Hazardous) for consistent styling |
| `fips_codes.py` | FIPS geographic code lookups for state/county filtering |
| `plot_utils.py` | Shared plotting helpers: hourly calendar heatmap and nighttime shading |
| `particulate_matter.py`, `ParticulateMatterHistogram.py` | Particulate-matter analysis helpers |

> `aqi_colors.py` and `plot_utils.py` are also imported by the sibling
> [`crocus`](https://github.com/gregorywanderson/crocus) repo (via a `sys.path`
> bridge), so keep them importable if you reorganize.

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **Note:** `cartopy` (used by `aqs_ozone_regional`) may require system-level
> dependencies. See the
> [cartopy install docs](https://scitools.org.uk/cartopy/docs/latest/installing.html)
> if you run into issues.

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

**NEIU rooftop: QuantAQ MODULAIR + Ambient Weather WS-500**
A rooftop pairing on BBH at NEIU's main campus. The QuantAQ MODULAIR low-cost
sensor measures PM1/PM2.5/PM10 and the gases CO, NO, NO₂, and O₃; the co-located
Ambient Weather WS-500 station provides wind and other meteorology. Pairing the
two allows wind-relative analysis (roses, lake-breeze diagnostics) with no
sensor-to-sensor displacement. `modulair_examples.ipynb` shows basic MODULAIR
access; `neiu_ozone_study.ipynb` is the paired analysis.

> CROCUS urban-network work has moved to the separate
> [`crocus`](https://github.com/gregorywanderson/crocus) repository.

---

## Dependencies

| Package | Purpose |
|---|---|
| `pyaqsapi` | EPA AQS DataMart API client |
| `pandas` / `numpy` | Data manipulation |
| `matplotlib` | Plotting |
| `cartopy` | Geospatial map projections |
| `suntime` | Sunrise/sunset times (for diurnal shading) |
| `windrose` | Wind and pollutant roses (`neiu_ozone_study`) |
| `pytz` | Timezone handling (NEIU local-time analysis) |
| `python-dotenv` | Loading API credentials from `.env` |

See `requirements.txt` for the installable list.

---

## Planned / in-progress

- **AirBeam + HabitatMap.** Low-cost mobile air-quality sensing via
  [HabitatMap](https://www.habitatmap.org/) and AirBeam devices. Initial
  downloader work is in `habitatmapdownloader.ipynb`; analysis notebooks are
  planned.
