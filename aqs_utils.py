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
  