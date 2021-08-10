# MS-noise-eraser
Mass spectrometers generates thousands of MS and MS/MS spectra in a single acquisition. However, there will be many repetitive and low intensity peaks (m/z values) considered as background or noise peaks. In order to get accurate identification of proteins and metabolites it is always adviced to remove such peaks from the raw data as they interfer in the database/ spectral library search and results in the identification of increased number false positives.

Here, we have developed a python package to remove such noise from the raw MGF files.

```
>python noise_remover.py -h
usage: noise_remover.py [-h] -ip [-ip ...] -t [-t ...]

Remove MS/MS peaks below the threshold limit from a .mgf file

positional arguments:
  -ip         MGF file path or path to multiple MGF files
  -t          m/z peaks with or less than the set threshold intensity values
              will be discarded

optional arguments:
  -h, --help  show this help message and exit
```
