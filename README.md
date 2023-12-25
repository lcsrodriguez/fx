# FOREX tick/candle high-frequency data tool

<img src="https://img.shields.io/static/v1?label=Range&message=Public&color=007bff"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Languages&message=Python&color=ff0000"/>&nbsp;&nbsp;<img src="https://img.shields.io/static/v1?label=Restriction&message=YES&color=26c601"/>

![GitHub release (latest by date)](https://img.shields.io/github/v/release/lcsrodriguez/fx)  &nbsp;![python version | 3.10+](https://img.shields.io/badge/python%20version-3.10+-magenta) &nbsp; [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

![](https://img.shields.io/badge/Dependabot-enabled-blue)

## Overview

This repository introduces a Python-based tool to retrieve high-frequency datasets on foreign exchange transactions.
One may either select to retrieve tick-by-tick or candle data for several frequencies in various formats.


**Remarks**:
- Timestamps provided in the tool are in *UTC+0*

<table align="center">
<tr>
    <td colspan="2">
      <b>DISCLAIMER</b>
    </td>
  </tr>
  <tr><td valign="top" width="100%">
    <ul>
        <li>Past performance is <b>not</b> indicative of future results.</li>
        <li>Data points are <b>indicative</b> and based on the lowest spreads available on the exchange.</li>
        <li>Datasets are provided <b><i>as is</i></b> for informational purposes only, and is <b>not</b> intended for trading purposes or financial, investment, tax, legal, ...</li>
    </ul>
 </tr>
</table>

## Getting started

```
cd examples/
python3 main.py
```

## Architecture

```
./
├── LICENSE
├── Makefile
├── README.md
├── docs/
│   └── ROADMAP.md
├── examples/
│   ├── main.ipynb
│   └── main.py
├── fxdata/
│   ├── Config.py
│   ├── FXData.py
│   ├── __init__.py
│   ├── constants.py
│   └── utils.py
├── out/
│   ├── csv/
│   └── parquet/
├── requirements.txt
├── setup.py
└── tmp/
```

## License & Credits


[MIT](LICENSE)