# ARTS tools
[![DOI](https://zenodo.org/badge/254329373.svg)](https://zenodo.org/badge/latestdoi/254329373)
[![PyPI version](https://badge.fury.io/py/arts-tools.svg)](https://badge.fury.io/py/arts-tools)
![CI](https://github.com/loostrum/arts_tools/workflows/CI/badge.svg)  
Scripts for handling Apertif Radio Transient System data.

## Dependencies
* python >= 3.6
* numpy >= 1.17
* astropy
* psrqpy
* python-irodsclient (optional)
* [psrdada-python](https://github.com/TRASAL/psrdada-python) (only for converting raw IQUV data to PSRFITS)
* [dadafits](https://github.com/TRASAL/dadafits) (only for converting raw IQUV data to PSRFITS)

## Installation
`pip install arts_tools`   
or   
`pip install arts_tools[irods]`   
to include the iRODS tools necessary for directly downloading files from the archive 
(ASTRON internal use only).

## Usage
An overview of the scripts included in this package is given below. Each script has as `-h` option that lists 
all available options.

For those that prefer using these tools from within Python, an overview of all functions and their usage is available
at https://loostrum.github.io/arts_tools.

## Finding known pulsars in the Apertif field-of-view
To find which pulsars are within the field of a given pointing, run 
`arts_find_pulsars_in_field --ra hh:mm:ss.s --dec dd:mm:ss.s`. This tool also prints in which 
compound beam the pulsars should be, so you only need to download those CBs from the archive instead of the
entire observation. \
To convert the tied-array beam data, which have frequency-and time-dependent pointing,
to a beam tracking a single point on the sky, use [arts_tracking_beams](https://github.com/loostrum/arts_tracking_beams). 


## Downloading files from the Apertif Long-Term Archive (ALTA)
Observations are identified by a unique task ID. To download all tied-array beams of a single compound beam to 
the current directory, run
`arts_download_from_alta --taskid <taskid> --cbs <cb_index>`. The default data release is the 2019 Science Verification 
Campaign (SVC). To change this, use the `--release` option. 

To download data directly from ALTA using iRODS, use `--release internal`. This requires that the user has set 
up their iRODS environment for communication with ALTA. 


## Reading parametersets
The FITS headers contain an encoded observation parameterset. To print the parameterset, use 
`arts_read_parameterset file.fits`. It can also be loaded in python as a dictionary with:
```python
from arts_tools import read_parameterset
parset = read_parameterset('/path/to/file.fits')
```
Note that all values are read as strings.

## Fixing archival FITS files
FITS files retrieved from the ALTA from before 2020/04/08 can be made readable with 
`arts_fix_fits_from_before_20200408 file.fits`. These fixes are applied:
1. The NAXIS2 value in the header is changed from zero to the correct value
2. The data size is expressed in bytes instead of bits
3. The frequency and time axes of the data are swapped
4. The frequency order of the data and weights, scales, offsets, and frequencies columns is flipped

By default, the script appends `_fixed` to the filename. Run `arts_fix_fits_from_before_20200408 -h` for more options.

#### Note for Science Verification Campaign data
Data from the SVC has a correct NAXIS2 value in some cases. However, the other fixes do need to be applied. 
This can be forced by running `arts_fix_fits_from_before_20200408 --force file.fits`.

## Converting raw IQUV data to PSRFITS
IQUV data are initially written to disk as-is with PSRDADA's `dada_dbdisk`. To convert these to PSRFITS with `dadafits`, 
use `arts_psrdada_iquv_to_fits --sb <space-separated synthesised beam list> --output_dir <output directory> <input psrdada file>`.
Instead of writing synthesised beams, the script can also write all tied-array beams. To do this, specifcy `--tab` instead 
of `--sb`. If `--sb` is the last option before the path to the psrdada files, add `--` like this: 
`arts_psrdada_iquv_to_fits --sb 35 36 -- input.dada`, otherwise the input files will be added to the SB list and the script will crash.
Run `arts_psrdada_iquv_to_fits -h` for more options.
