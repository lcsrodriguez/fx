# FOREX tick/candle high-frequency data tool

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
python3 examples.py
```

## Architecture

```
.
├── LICENSE
├── README.md
├── examples/
│   └── example.py
├── fx/
│   ├── __init__.py
│   ├── constants.py
│   └── main.py
├── out/
│   ├── csv/
│   └── parquet/
├── requirements.txt
├── setup.py
└── tmp/
```

## License


[MIT](LICENSE)