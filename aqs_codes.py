class AQSParameter:
    def __init__(self, code, name, symbol, units):
        self.code   = code
        self.name   = name
        self.symbol = symbol
        self.units  = units
    
    def __str__(self):
        return self.code
    
    def __repr__(self):
        return f"<AQSParameter {self.name} ({self.code})>"

o3        = AQSParameter("44201", "Ozone",             "O\u2083",  "ppm")
no2       = AQSParameter("42602", "Nitrogen Dioxide",  "NO\u2082", "ppb")
co        = AQSParameter("42101", "Carbon Monoxide",   "CO",       "ppm")
so2       = AQSParameter("42401", "Sulfur Dioxide",    "SO\u2082", "ppb")
pm25      = AQSParameter("88101", "PM 2.5",            "PM\u2082.\u2085", "µg/m³")
pm10      = AQSParameter("88102", "PM 10",             "PM\u2081\u2080", "µg/m³")

solar_rad = AQSParameter("63301", "Solar Radiation",   "SR",       "W/m²")
uv_rad     = AQSParameter("63302", "Ultraviolet",      "UV",       "W/m²")
#temp      = AQSParameter("62101", "Temperature",       "T",        "°C")
#mxht      = AQSParameter("61301", "Mixing Height", "km")
#WIND_Sp   = AQSParameter("61101", "Wind Speed -scalar", "")
#WIND_DIR  = AQSParameter("61102", "Wind Direction -scalar", "")
#WIND_DIR_RES = AQSParameter("61104", "Wind Direction -Resultant", "")
#WIND_GUST = AQSParameter("61105", "Peak Wind Gust", "")

#HAPS_CH2O = "43502" # formaldehyde
#HNO3 = "42305" # Nitric Acid AQS Parameter Code


