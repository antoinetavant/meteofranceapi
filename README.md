# MeteoFrance_PublicAPI: A Python Wrapper for the MétéoFrance API !

![Supported Python versions](https://img.shields.io/pypi/pyversions/meteofrance-publicapi.svg?color=%2334D058) ![License](https://img.shields.io/pypi/l/meteofrance-publicapi
) ![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/antoinetavant/meteofranceapi/python-test.yml)


python wrapper of the portail-api.meteofrance.fr datasets

It especially allows to manage easily the API key.

**Documentation**:  [antoinetavant.github.io/meteofranceapi](https://antoinetavant.github.io/meteofranceapi/) (WIP)

**Source Code**: [github.com/antoinetavant/meteofranceapi](https://github.com/antoinetavant/meteofranceapi)

## Disclaimer

The tool is not officially provided by MétéoFrance.

It is build by trials-and-errors and revers-engineering by an amateur.

Most of the functionalities should work, but it may not be the best way to achieve it.

# Installation

Using `pip`
```
pip install meteofrance-publicapi
```

# Usage
To use the ressources, you need an account at MeteoFrance. It is free (as in free-beer).

## How to get the API key
First register on [portail-api.meteofrance.fr](https://portail-api.meteofrance.fr/)

Once your account is activated, several options are possible to use `meteofrance-publicapi` :
- an API key for the API requested
- a token for the API requested (limited to max 1 hour)
- an Application ID to the classes which will manage the API token.

The Application ID is the recommended use, as it allows to requests dynamically new tokens.

However, you need to keep it a secret !

### Obtaining the Application ID

From the website  [portail-api.meteofrance.fr](https://portail-api.meteofrance.fr/)
- click on the _Bonjour User Name_ button (upper right corner)
- click _Mes API_
- click "Générer Token" for _any API_
- scroll down to the `curl` field
- The Application Key is the last field of the curl commend :
    `curl -k -X POST [... ... ...] "Authorization: Basic <YourAPPLICATION_ID>`


## Examples

### Accessing observation data

Observation data are measured by a station. The list of the stations can be accessed by

```python
import meteofrance_publicapi as mpa
observation_client = mpa.Observations(application_id=<YourApplicationID>)
observation_client.list_stations()
```
|   | Id_station | Id_omm   | Nom_usuel | Latitude                | Longitude  | Altitude   | Date_ouverture | Pack       |
|-----| -------|----------|-----------|-------------------------|------------|------------|----------------|------------|
| 0          | 01014002 | NaN       | ARBENT                  | 46.278167  | 5.669000   | 534            | 2003-10-01 | RADOME |
| 1          | 01027003 | NaN       | BALAN_AERO              | 45.833000  | 5.106667   | 196            | 2014-05-26 | ETENDU |
| 2          | 01034004 | NaN       | BELLEY                  | 45.769333  | 5.688000   | 330            | 2001-09-13 | RADOME |
| 3          | 01064001 | NaN       | VERIZIEU                | 45.777167  | 5.487167   | 281            | 2015-01-01 | ETENDU |
| 4          | 01071001 | NaN       | CESSY                   | 46.310333  | 6.080333   | 507            | 2002-05-01 | RADOME |
| ...        | ...      | ...       | ...                     | ...        | ...        | ...            | ...        | ...    |
| 2098       | 98832004 | 91588     | MTGNE SOURCES           | -22.143833 | 166.593167 | 773            | 1989-08-01 | ETENDU |
| 2099       | 98832005 | NaN       | OUINNE                  | -21.984000 | 166.680500 | 54             | 1974-01-01 | ETENDU |
| 2100       | 98832006 | NaN       | RIVIERE BLANCHE         | -22.132667 | 166.726333 | 171            | 2000-11-01 | ETENDU |
| 2101       | 98832101 | NaN       | GORO_ANCIENNE_PEPINIERE | -22.269167 | 166.967500 | 298            | 1995-01-01 | ETENDU |
| 2102       | 98833002 | NaN       | MEA                     | -21.455500 | 165.767333 | 571            | 1988-01-01 | ETENDU |

### Accessing Arome Forecasts

See the notebook [Arome Forecast](./doc/examples/arome.ipynb) for examples of accessing the forecast of the AROME model.

# TODO

- [ ] Add local cache capabilities, for instance with [joblib](https://joblib.readthedocs.io/en/stable/memory.html)
- [ ] Add persistent storage, locally or with a could provider
