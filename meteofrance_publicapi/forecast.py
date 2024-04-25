from pathlib import Path
import xmltodict
from .errors import MissingDataError
import logging
from .core import MeteoFranceAPI

logger = logging.getLogger(__name__)

#: The available territories for the AROME model.
AVAILABLE_AROME_TERRITORY = [
    "FRANCE",
    "NCALED",
    "INDIEN",
    "POLYN",
    "GUYANE",
    "ANTIL",
]

AVAILABLE_ARPEGE_TERRITORY = [ "EUROPE", "GLOBE", "ATOURX", "EURAT"]
RELATION_TERRITORY_TO_PREC_ARPEGE = {"EUROPE": 0.1,
                                     "GLOBE": 0.25,
                                     "ATOURX": 0.1,
                                     "EURAT": 0.05}

precision_float_to_str = {0.25: "025", 0.1: "01", 0.05: "005", 0.01: "001", 0.025: "0025"}



class AromeForecast(MeteoFranceAPI):
    """Access the AROME numerical Forcast.

    Parameters
    ----------
    precision : {0.01, 0.025}, optional
        the resolution of the AROME Model, by default 0.01
    territory : str, optional
        The AROME territory to fetch, by default "FRANCE"
    api_key : str | None, optional
        The API Key, by default None
    token : str | None, optional
        The API Token, by default None
    application_id : str | None, optional
        The Application ID, by default None
    cache_dir : str | None, optional
        The path to the caching directory, by default None.
        If None, the cache directory is set to "/tmp/cache".

    Note
    ----
    See :class:`.MeteoFranceAPI` for the parameters `api_key`, `token` and `application_id`.

    The available territories are listed in :data:`.AVAILABLE_TERRITORY`.

    Usage
    =====

    1. Fetch the capabilities
    -------------------------

    Use the method ``get_capabilities`` to access the available data.

    2. Get the coverage
    -------------------

    The coverage means the data fields available.
    Such a field is the temperature.

    use ``get_coverage`` to fetch the coverage.

    """

    api_version = "1.0"
    base_url = "https://public-api.meteofrance.fr/public/arome/" + api_version

    def __init__(
        self,
        precision: float = 0.01,
        territory: str = "FRANCE",
        api_key: str | None = None,
        token: str | None = None,
        application_id: str | None = None,
        cache_dir: str | None = None,
    ):
        """Init the AromeForecast object.

        Parameters
        ----------
        precision : {0.01, 0.025}, optional
            the resolution of the AROME Model, by default 0.01
        territory : str, optional
            The AROME territory to fetch, by default "FRANCE"
        api_key : str | None, optional
            The API Key, by default None
        token : str | None, optional
            The API Token, by default None
        application_id : str | None, optional
            The Application ID, by default None
        cache_dir : str | None, optional
            The path to the caching directory, by default None.
            If None, the cache directory is set to "/tmp/cache".

        Note
        ----
        See :class:`.MeteoFranceAPI` for the parameters `api_key`, `token` and `application_id`.

        The available territories are listed in :data:`.AVAILABLE_TERRITORY`.

        """
        super().__init__(api_key, token, application_id)
        cache_dir = cache_dir or "/tmp/cache"
        self.cache_dir = Path(cache_dir)
        self.precision = precision  # the precision of the AROME model, in Degrees. Can be 0.01 or 0.025
        self.territory = territory  # the territory of the forecast. Can be "FRANCE" or "ANTIL" or others (see the API documentation)
        self.data_capabilities = None
        self.all_coverageid_prefix = None # the list of all coverage ID prefix
        self.all_coverageid = None # the list of all coverage ID
        self._validate_parameters()

    def _validate_parameters(self):
        """Assert the parameters are valid."""
        if self.precision not in [0.01, 0.025]:
            raise ValueError("The parameter precision must be 0.01 or 0.025")
        if self.territory not in AVAILABLE_AROME_TERRITORY:
            raise ValueError(
                f"The parameter precision must be in {AVAILABLE_AROME_TERRITORY}"
            )

    @property
    def entry_point(self):
        """The entry point to the AROME service."""
        return f"wcs/MF-NWP-HIGHRES-AROME-{precision_float_to_str[self.precision]}-{self.territory}-WCS"

    @property
    def entry_point_capabilities(self):
        """The entry point to the capabilities of the AROME service."""
        return self.entry_point + "/GetCapabilities"

    @property
    def entry_point_getcoverage(self):
        """The entry point to get the coverage of the AROME service."""
        return self.entry_point + "/GetCoverage"

    @property
    def entry_point_describecoverage(self):
        """The entry point to describe the coverage of the AROME service."""
        return self.entry_point + "/DescribeCoverage"

    @property
    def capabilities(self):
        """The Capabilities of the AROME service."""
        if self.data_capabilities is None:
            url = f"{self.base_url}/{self.entry_point_capabilities}"
            params = {
                "service": "WCS",
                "version": "2.0.1",
                "language": "eng",
            }
            try :
                response = self._get_request(url, params=params)
            except MissingDataError as e:
                logger.error(f"Error fetching the capabilities: {e}")
                logging.error(f"URL: {url}")
                logging.error(f"Params: {params}")
                raise e
            xml = response.text
            try:
                self.data_capabilities = xmltodict.parse(xml)
            except MissingDataError as e:
                logger.error(f"Error parsing the XML response: {e}")
                logger.error(f"Response: {xml}")
                raise e
        return self.data_capabilities

    def get_capabilities(self):
        """Get the capabilities of the service.
        In particular, lists the available coverages IDs,
        that is a mandatory parameter for the get_coverage request."""
        list_capabilities = self.capabilities["wcs:Capabilities"]["wcs:Contents"]["wcs:CoverageSummary"]
        self.all_coverageid = [capabiltity["wcs:CoverageId"] for capabiltity in list_capabilities]
        self.all_coverageid_prefix = list({coverageid.split("___")[0] for coverageid in self.all_coverageid})

    def all_coverageid_of_name(self, coverage_name):
        """Return the list of all coverage ID of a given name.

        Parameters
        ----------
        coverage_name : str
            The name of the coverage. For example "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND".
            Availables names are is :attr:`all_coverageid_prefix`.

        Returns
        -------
        list[str]
            the list of all coverage ID of the given name.
        """
        coverage_ids = [
            coverageid
            for coverageid in self.all_coverageid
            if coverageid.startswith(coverage_name)
        ]
        if not coverage_ids:
            raise ValueError(f"No coverage ID found for {coverage_name}")
        return sorted(coverage_ids)

    def get_description(self, coverageid=None):
        """Get the description of a coverage.

        .. warning::
            The return value is the raw XML data.
            Not yet parsed to be usable.
            In the future, it should be possible to use it to
            get the available heights, times, latitudes and longitudes of the forecast.

        Parameters
        ----------
        coverageid: str, optional
            the Coverage ID. Use :meth:`get_coverage` to access the available coverage ids.
            By default use the latest temperature coverage ID.

        Returns
        -------
        description : dict
            the description of the coverage.
        """
        if coverageid is None:
            coverageid_prefix_temperature = (
                "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND"
            )
            coverageid = self.all_coverageid_of_name(coverageid_prefix_temperature)[-1]
        url = f"{self.base_url}/{self.entry_point_describecoverage}"
        params = {
            "service": "WCS",
            "version": "2.0.1",
            "coverageid": coverageid,
        }
        response = self._get_request(url, params=params)
        description = xmltodict.parse(response.text)
        return description

    def get_coverage(
        self,
        coverageid=None,
        height=2,
        time=0,
        lat=(37.5, 55.4),  # roughly the latitudes of France
        long=(-12, 16),  # roughly the longitudes of France
    ):
        """Fetch the raster values of the model predictions.

        The raster is saved to a file in the cache directory.

        Parameters
        ----------
        coverageid: str, optional
            the Coverage ID. Use :meth:`get_coverage` to access the available coverage ids.
            By default use the latest temperature coverage ID.
        height: int, optional
            the height in meters of the model. By default 2 meters above ground.
            The available height could be accessed from the API but it is not implemented yet.
        time: int, optional
            the forecast time (how much in the future).
            By default 0s in the future.
            The available forecast time can be known (not implemented yet)
        lat: tuple[float], optional
            The min et max latitude to return.
            By default, the France latitudes
        long: tuple[float], optional
            the min and max longitude to return.
            By default, the France longitude.

        Returns
        -------
        filename : pathlib.Path
            the path to the file containing the Tiff image.

        .. see-also::
           :func:`.aster.plot_tiff_file` to plot the file.
        """
        if coverageid is None:
            coverageid_prefix_temperature = (
                "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND"
            )
            coverageid = self.all_coverageid_of_name(coverageid_prefix_temperature)[-1]
        filename = f"{height}m_{time}Z_{lat[0]}-{lat[1]}_{long[0]}-{long[1]}.tiff"
        filepath = self.cache_dir / coverageid / filename
        logger.debug(f"{filepath=}")
        if not filepath.exists():
            logger.debug("File not found in Cache, fetching data")
            url = f"{self.base_url}/{self.entry_point_getcoverage}"
            params = {
                "service": "WCS",
                "version": "2.0.1",
                "coverageid": coverageid,
                "format": "image/tiff",
                "subset": [
                    f"height({height})",  # the height of the forecast, in meters
                    f"time({time})",  # the initial time of the forecast
                    f"lat({lat[0]},{lat[1]})",
                    f"long({long[0]},{long[1]})",
                ],
                "geotiff:compression": "DEFLATE",  # compression of the tiff file
            }
            response = self._get_request(url, params=params)
            # save res.text to tiff file
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as f:
                f.write(response.content)
        return filepath


class ArpegeForecast(AromeForecast):
    api_version = "1.0"
    base_url = "https://public-api.meteofrance.fr/public/arpege/" + api_version

    def __init__(
        self,
        territory: str = "EUROPE",
        api_key: str | None = None,
        token: str | None = None,
        application_id: str | None = None,
        cache_dir: str | None = None,
    ):
        """Init the ArpegeForecast object.

        Parameters
        ----------
        territory : str, optional
            The ARPEGE territory to fetch, by default "FRANCE"
        api_key : str | None, optional
            The API Key, by default None
        token : str | None, optional
            The API Token, by default None
        application_id : str | None, optional
            The Application ID, by default None
        cache_dir : str | None, optional
            The path to the caching directory, by default None.
            If None, the cache directory is set to "/tmp/cache".

        Note
        ----
        See :class:`.MeteoFranceAPI` for the parameters `api_key`, `token` and `application_id`.

        The available territories are listed in :data:`.AVAILABLE_TERRITORY`.

        """
        super(AromeForecast, self).__init__(api_key, token, application_id)
        cache_dir = cache_dir or "/tmp/cache"
        self.cache_dir = Path(cache_dir)
        self.precision = RELATION_TERRITORY_TO_PREC_ARPEGE[territory]  # the precision of the ARPEGE model, in Degrees.
        self.territory = territory  # the territory of the forecast.
        self.data_capabilities = None
        self.all_coverageid_prefix = None # the list of all coverage ID prefix
        self.all_coverageid = None # the list of all coverage ID
        self._validate_parameters()

    def _validate_parameters(self):
        """Assert the parameters are valid."""
        if self.territory not in AVAILABLE_ARPEGE_TERRITORY:
            raise ValueError(
                f"The parameter precision must be in {AVAILABLE_ARPEGE_TERRITORY}"
            )

    @property
    def entry_point(self):
        """The entry point to the AROME service."""
        return f"wcs/MF-NWP-GLOBAL-ARPEGE-{precision_float_to_str[self.precision]}-{self.territory}-WCS"
