Install `pip install -i https://test.pypi.org/simple/ econdatapy` and then run with `python`

Note: if *ECONDATA_CREDENTIALS* environment variable is not set you will be prompted for an API token which can be retrieved from the  *Account* page at [www.econdata.co.za](https://www.econdata.co.za).


```
>>> from econdatapy import read

>>> x = read.dataset("MINING")
Fetching dataset(s) - MINING

Processing data set: ECONDATA-MINING-1.1.0

>>> x["metadata"]
{'agencyid': 'ECONDATA', 'id': 'MINING', 'version': '1.1.0', 'name': ['en', 'Mining'], 'provision-agreement': ['#sdmx.infomodel.registry.ProvisionAgreeme
ntRef', {'agencyid': 'ECONDATA', 'id': 'MINING_ECONDATA_STATSSA', 'version': '1.1.0'}], 'SOURCE_DATASET': 'P2041', 'RELEASE': 'Unreleased'}

>>> y = x["data"]

>>> y["MIN001.I.N"]
    TIME_PERIOD  OBS_VALUE
0    1980-01-01      105.2
1    1980-02-01      105.6
2    1980-03-01      105.1
3    1980-04-01      105.8
4    1980-05-01      108.7
..          ...        ...
525  2023-10-01       96.0
526  2023-11-01       99.9
527  2023-12-01       88.5
528  2024-01-01       80.7
529  2024-02-01       82.9

[530 rows x 2 columns]

>>> y["MIN001.I.N"].metadata
{'MNEMONIC': 'MIN001', 'FREQ': 'M', 'BASE_PER': '2019', 'series-key': 'MIN001.I.N', 'MEASURE': 'I', 'SEASONAL_ADJUST': 'N', 'UNIT_MEASURE': 'Index', 'SOU
RCE_IDENTIFIER': 'FMP20000', 'LABEL': 'Total, gold included'}
```
