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
        csv_sting =  self.session.get(url).text
        data = pd.read_csv(StringIO(csv_sting), sep=";", dtype=str)
        numerical_columns = ["Latitude", "Longitude", "Altitude"]
        data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric)
        datetime_columns = ["Date_ouverture"]
        data[datetime_columns] = data[datetime_columns].apply(pd.to_datetime)
        return data

    def get_station_horaire(self,
                            station_id: str,
                            datetime: str | None = None):
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
        req =  self.session.get(url, params=params)
        #TODO : add req status code check
        csv_sting = req.text
        data = pd.read_csv(StringIO(csv_sting), sep=";")
        return data
