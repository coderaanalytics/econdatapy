Requires the `requests` and `pandas` packages, install and then run with `ECONDATA_CREDENTIALS="username;password" python`


```
>>> from read_dataset import read_dataset
>>> x = read_dataset("MINING")
Fetching dataset(s) - MINING

Processing data set: ECONDATA-MINING-1.1.0

>>> x[0]
    TIME_PERIOD  OBS_VALUE
0    2003-01-01     7558.5
1    2003-02-01     8028.6
2    2003-03-01     7168.1
3    2003-04-01     7101.3
4    2003-05-01     6407.8
..          ...        ...
249  2023-10-01    56122.3
250  2023-11-01    59065.4
251  2023-12-01    59191.1
252  2024-01-01    56687.9
253  2024-02-01    56604.1

[254 rows x 2 columns]
>>> x[0].metadata
{'MNEMONIC': 'MIN002', 'UNIT_MULT': '6', 'FREQ': 'M', 'series-key': 'MIN002.S.S', 'MEASURE': 'S', 'SEASONAL_ADJUST': 'S', 'UNIT_MEASURE': 'Rand', 'SOURCE
_IDENTIFIER': 'MVS20001', 'LABEL': 'Total, gold excluded'}
```
