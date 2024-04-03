"""Core module for the meteofranceapi package."""
from pathlib import Path
import time
import requests
import logging

logger = logging.getLogger(__name__)

class MeteoFranceAPI:
    def __init__(self,
                 api_key: str | None = None,
                 token: str | None = None,
                 application_id: str | None = None,
                 ):
        """Init the MeteoFranceAPI object.
        """
        self.api_key = api_key
        self.token = token
        self.application_id = application_id
        self.connect()

    def connect(self):
        """Connect to the meteo-France API.

        If the API key is provided, it is used to authenticate the user.
        If the token is provided, it is used to authenticate the user.
        If the username and password are provided, a token is requested from the API.
        """
        if self.api_key is None and self.token is None:
            if self.application_id is None:
                raise ValueError("api_key or token or application_id must be provided")
            self.token = self.get_token()

        self.session = requests.Session()
        if self.api_key is not None:
            logger.debug("using api key")
            self.session.headers.update({"apikey": self.api_key})
        else:
            logger.debug("using token")
            self.session.headers.update({"Authorization": "Bearer " + self.token})

    def get_token(self):
        """request a token from the meteo-France API.

        The token lasts 1 hour, and is used to authenticate the user.
        If a new token is requested before the previous one expires, the previous one is invalidated.
        A local cache is used to avoid requesting a new token at each run of the script.
        """
        # cache the token for 1 hour
        TOKEN_DURATION_S = 3600
        local_tmp_cache = Path("/tmp/correction_climatique/meteofrance/arome/")
        cachefilename = local_tmp_cache / "token.txt"
        cachetimefilename = local_tmp_cache / "token_time.txt"

        if cachefilename.exists() and cachetimefilename.exists():
            print("reading token from cache")
            with open(cachetimefilename) as f:
                cachetime = float(f.read())
            if cachetime >= (time.time() - TOKEN_DURATION_S ):
                with open(cachefilename) as f:
                    token = f.read()
                return token

        token_entrypoint = " https://portail-api.meteofrance.fr/token"
        params = {"grant_type": "client_credentials"}
        header = {"Authorization": "Basic " + self.application_id}
        res = requests.post(token_entrypoint,
                                   params=params,
                                   headers=header
                                   )
        self.token = res.json()["access_token"]
        # save token to file
        local_tmp_cache.mkdir(parents=True, exist_ok=True)
        with open(cachefilename, "w") as f:
            f.write(self.token)
        with open(cachetimefilename, "w") as f:
            f.write(str(time.time()))

