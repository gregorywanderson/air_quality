import pandas as pd

def wrangle_aqs_timeseries(tdata, name=None):
    label = f" ({name})" if name else ""
    
    if tdata is None or tdata.empty:
        raise ValueError(f"Empty or None DataFrame{label} — API call likely returned no data")
    
    missing = [c for c in ["date_local", "time_local", "date_gmt", "time_gmt"] 
               if c not in tdata.columns]
    if missing:
        raise ValueError(f"Missing columns{label}: {missing}\n"
                         f"Available columns: {list(tdata.columns)}")
    
    tdata["datetime_local"] = tdata["date_local"] + " " + tdata["time_local"]
    tdata["datetime_gmt"]   = tdata["date_gmt"]   + " " + tdata["time_gmt"]
    tdata["datetime_local"] = pd.to_datetime(tdata["datetime_local"], 
                                             format="%Y-%m-%d %H:%M", utc=False)
    tdata["datetime_gmt"]   = pd.to_datetime(tdata["datetime_gmt"],   
                                             format="%Y-%m-%d %H:%M", utc=True)
    return tdata
  
def download_daily_summary(station_key, parameter, stations,
                           state_fips, county_fips, start_dt, end_dt, aqs):
    """Download the AQS daily summary for one parameter at one station."""
    station = stations[station_key]
    return aqs.bysite.dailysummary(
        parameter=parameter.code,
        bdate=start_dt,
        edate=end_dt,
        stateFIPS=state_fips,
        countycode=county_fips,
        sitenum=station["site_number"],
    )

def download_hourly_data(station_key, parameter, stations,
                         state_fips, county_fips, start_dt, end_dt, aqs,
                         year=None):
    """Download and prepare one year of hourly AQS measurements.

    Filters to 1-hour sample duration and returns a time-sorted frame with
    parsed datetime columns.

    Parameters
    ----------
    station_key : str
        Key into ``stations``.
    parameter : object
        Parameter object exposing ``.code`` and ``.name`` (e.g. o3, no2).
    stations : dict
        Mapping station_key -> dict with "site_number" and "name".
    state_fips, county_fips : str
        AQS FIPS codes.
    start_dt, end_dt : datetime.datetime
        Inclusive query range.
    aqs : module
        pyaqsapi handle.
    year : int, optional
        Only used to make the "no data" error message clearer.

    Returns
    -------
    pd.DataFrame
        1-hour records, sorted by datetime_local, index reset.
    """
    station = stations[station_key]

    data = aqs.bysite.sampledata(
        parameter=parameter.code,
        bdate=start_dt,
        edate=end_dt,
        stateFIPS=state_fips,
        countycode=county_fips,
        sitenum=station["site_number"],
    )

    data = wrangle_aqs_timeseries(
        data, name=f"{station['name']} {parameter.name}",
    )

    hourly_data = data.loc[data["sample_duration"].eq("1 HOUR")].copy()

    if hourly_data.empty:
        when = f" in {year}" if year is not None else ""
        raise ValueError(
            f"No 1-hour {parameter.name} data were returned for "
            f"{station['name']}{when}."
        )

    return hourly_data.sort_values("datetime_local").reset_index(drop=True)