
import requests
from pathlib import Path
import rasterio
from .core import MeteoFranceAPI

class AromeForcast(MeteoFranceAPI):

    base_url = "https://public-api.meteofrance.fr/public/arome/1.0"
    entry_point_getcapabilities = "wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCapabilities"
    entry_point_getcoverage = "wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage"
    apikey: str = None  # can be generated from the user interface by selecting API Key

    def __init__(self, api_key: str | None = None,
                 token: str | None = None,
                 application_id: str | None = None,
                 cache_dir: str | None = None):
        super().__init__(api_key, token, application_id)
        self.cache_dir = Path(cache_dir) or Path("/tmp/cache")

    def get_capabilities(self):
        """Get the capabilities of the service.
        In particlare, lists the available coverages IDs,
        that is a mandatory parameter for the get_coverage request."""
        import xmltodict
        url = f"{self.base_url}/{self.entry_point_getcapabilities}"
        params = {
            "service": "WCS",
            "version": "2.0.1",
            "language": "eng",
        }
        response = self.session.get(url, params=params)
        if response.status_code != 200:
            print(response.text)
            raise RuntimeError(f"Request failed with status code {response.status_code}")
        xml = response.text
        data_capabilities = xmltodict.parse(xml)
        list_capabilities = data_capabilities['wcs:Capabilities']['wcs:Contents']['wcs:CoverageSummary']
        self.all_coverageid_prefix = list( { coverageid['wcs:CoverageId'].split("___")[0] for coverageid in list_capabilities } )
        coverageid_prefix_temperature = "TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND"
        self.temperature_coverageid = [ coverageid['wcs:CoverageId'] for coverageid in list_capabilities if coverageid['wcs:CoverageId'].startswith(coverageid_prefix_temperature) ]
        self.latest_temperature_coverageid = self.temperature_coverageid[-1]

    def get_coverage(self):
        """Fetch the raster values of the model predictions.
        For now, only fetch the last temperature prediction.

        The raster is saved to a file in the cache directory.

        Returns
        -------
        temperature : np.ndarray
            the temperature in °C
        transform : rasterio.transform
            the affine transform of the raster
        filename : pathlib.Path
            the path to the file containing the raster
        """
        filename = self.cache_dir / self.latest_temperature_coverageid / "temperature_2m_0Z.tiff"
        print(filename)
        if not filename.exists():
            print("fetching data")
            url = f"{self.base_url}/{self.entry_point_getcoverage}"
            params = {
                "service": "WCS",
                "version": "2.0.1",
                "coverageid": self.latest_temperature_coverageid,
                "format": "image/tiff",
                "subset": ["height(2)", # the height of the forecast, in meters
                        "time(0)", # the initial time of the forecast
                        "lat(37.5,55.4)",  # roughly the latitudes of France
                        "long(-12,16)", # roughly the longitudes of France
                        ],
                "geotiff:compression": "DEFLATE", # compression of the tiff file
            }


            response = self._get_request(url, params=params)

            #save res.text to tiff file
            filename.parent.mkdir(parents=True, exist_ok=True)
            with open(filename, "wb") as f:
                f.write(response.content)
        print("opening file")
        with rasterio.open(filename) as src:
            temperature = src.read(1, masked=True)
            transform = src.transform
        return temperature, transform, filename

    @staticmethod
    def plot_tiff_file(filename):
        """Illustrates how to open a file an to plot it."""
        import rasterio
        import matplotlib.pyplot as plt
        import cartopy.crs as ccrs
        import cartopy.feature as feature

        # Open the file:
        with rasterio.open(filename) as src:
            temperature = src.read(1, masked=True)
            transform = src.transform


        # Display the source image with cartopy using the geotransform from the source dataset
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        im = ax.imshow(temperature, cmap='jet', extent=[transform[2], transform[2] + transform[0]*temperature.shape[1], transform[5] + transform[4]*temperature.shape[0], transform[5]])

        ax.add_feature(feature.BORDERS.with_scale('10m'), color='black', linewidth=1)
        ax.add_feature(feature.COASTLINE.with_scale('10m'), color='black', linewidth=1)

        cbar = plt.colorbar(im, ax=ax, shrink=0.5)

        lyon_coord = [4.8357, 45.7640]
        paris_coord = [2.3522, 48.8566]

        ax.plot(lyon_coord[0], lyon_coord[1], 'bo', transform=ccrs.PlateCarree())
        ax.plot(paris_coord[0], paris_coord[1], 'bo', transform=ccrs.PlateCarree())

