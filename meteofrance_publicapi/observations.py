"""The interface for the observational data from the meteo-France API.

See :
- https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesObservation
- https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesPaquetObservation
"""
from io import StringIO
import logging

import pandas as pd
from .core import MeteoFranceAPI

logger = logging.getLogger(__name__)

NAME_EXPLICIT_EN_COMMON = {
    "lat": "latitude",
    "lon": "longitude",
    "t": "temperature_K",
    "u": "relative_humidity_%",
    "dd": "wind_direction_deg",
    "ff": "wind_speed_m_s-1",
    "t_10": "temperature_10cm_K",
    "t_20": "temperature_20cm_K",
    "t_50": "temperature_50cm_K",
    "t_100": "temperature_100cm_K",
    "vv": "visibility_m",
    "n": "nebulosity_%",
    "insolh": "sunshine_duration_min",
    "ray_glo01": "global_radiation_J_m-2",
}

NAME_EXPLICIT_EN_6min = {
    "dxi10": "mean_wind_gust_direction_deg",
    "fxi10": "mean_wind_gust_speed_m_s-1",
    "rr_per": "precipitation_6min_mm",
    "pres": "pressure_Pa",
    "pmer": "pressure_sea_level_Pa",
    "eta_sol": "status_code",
    "sss": "snow_depth_m",
}
NAME_EXPLICIT_EN_HOURLY = {
 "td": "dew_point_temperature_K",
 "tx": "max_temperature_K",
    "tn": "min_temperature_K",
    "ux": "max_relative_humidity_%",
    "un": "min_relative_humidity_%",
    "dxy": "max_wind_gust_direction_deg",
    "fxy": "max_wind_gust_speed_m_s-1",
    "dxi": "wind_direction_deg",
    "fxi": "wind_speed_m_s-1",
    "rr1": "precipitation_1h_mm",

}


class Observations(MeteoFranceAPI):
    """Wrapper around the meteo-France API for the observational data.

    It wrapps both the "station" and "paquet" endpoints.

    Ressources are:
    - list_stations
    - /station/horaire
    - /station/infrahoraire-6m
    - /paquet/infrahoraire-6m
    - /paquet/horaire
    - /paquet/stations/infrahoraire-6m
    - /paquet/stations/horaire

    Documentation
    -------------
    See:
    - https://portail-api.meteofrance.fr/web/fr/api/DonneesPubliquesPaquetObservation
    - https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=93&id_rubrique=32
    """

    base_url = "https://public-api.meteofrance.fr/public/DPObs/"
    version = "v1"

    def __init__(
        self,
        api_key: str | None = None,
        token: str | None = None,
        application_id: str | None = None,
    ):
        super().__init__(api_key, token, application_id)

    def list_stations(self):
        """Liste the available stations.

        Returns:
        --------
        pd.DataFrame: a DataFrame with the list of stations.

        """
        url = self.base_url + self.version + "/liste-stations"
        logger.debug(f"GET {url}")
        res = self._get_request(url)
        csv_sting =  res.text
        data = pd.read_csv(StringIO(csv_sting), sep=";", dtype=str)
        numerical_columns = ["Latitude", "Longitude", "Altitude"]
        data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric)
        datetime_columns = ["Date_ouverture"]
        data[datetime_columns] = data[datetime_columns].apply(pd.to_datetime)
        return data

    def get_station_horaire(self,
                            station_id: str,
                            datetime: str | None = None,
                            rename_columns: bool = True,):
        """Get the hourly data for a given station.

        Parameters:
        -----------
        station_id: str
            the id of the station
        datetime: str
            the date of the data, in the format ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
        format: {"json", "csv", "geojson"}
            the format of the data.

        Returns:
        --------
        pd.DataFrame: a DataFrame with the data.

        """
        url = self.base_url + self.version + "/station/horaire"
        params = {"id_station": station_id,
                  "format": "csv"}
        if datetime is not None:
            params["datetime"] = datetime
        logger.debug(f"GET {url}")
        req =  self._get_request(url, params=params)
        csv_sting = req.text
        data = pd.read_csv(StringIO(csv_sting), sep=";")
        if rename_columns:
            data = data.rename(columns=NAME_EXPLICIT_EN_COMMON)
            data = data.rename(columns=NAME_EXPLICIT_EN_HOURLY)
        return data

    def get_station_6min(self,
                         station_id: str,
                         datetime: str | None = None,
                         rename_columns: bool = True):
        """Get the 6min data for a given station.

        Parameters:
        -----------
        station_id: str
            the id of the station
        datetime: str
            the date of the data, in the format ISO 8601 (YYYY-MM-DDTHH:MM:SSZ)
        format: {"json", "csv", "geojson"}
            the format of the data.

        Returns:
        --------
        pd.DataFrame: a DataFrame with the data.

        """
        url = self.base_url + self.version + "/station/infrahoraire-6m"
        params = {"id_station": station_id,
                  "format": "csv"}
        if datetime is not None:
            params["datetime"] = datetime
        logger.debug(f"GET {url}")
        req =  self._get_request(url, params=params)
        csv_sting = req.text
        data = pd.read_csv(StringIO(csv_sting), sep=";")
        if rename_columns:
            data = data.rename(columns=NAME_EXPLICIT_EN_COMMON)
            data = data.rename(columns=NAME_EXPLICIT_EN_6min)
        return data
