# PK Date and Time Reconciliation

> Jupyter notebook that allows for date and time of PK data collection to be reconciled.

## Config File

Use the template config file as a handy quick start guide.

Config field mapping references:

- source [__DEPRECATED__]
  : The file path to the the medrio source file.
  - Needs to be a `.csv` file
  - e.g `"source": "./source.csv"`
- comparison [__DEPRECATED__]
  : The file path to the comparison file / vendor file
  - Needs to be a `.csv` file
  - e.g `"comparison": "./comparison.csv"`
- output [__DEPRECATED__]
  : The directory path to write all output to.
  - e.g `"output": "./output"`
- match [__REQUIRED__]
  : An `object` that maps timepoints to their _date_ and _time_ variable descriptors.
  - e.g
    ```
    {
      "match": {
        "0": {"date": "PKPDDat_C", "time": "PKPDTim_C"},
        "0.25": {"date": "PK15Dat_C", "time": "PK15Tim_C"},
      }
    }
    ```

__Note:__
The _jupyter notebook_ creates a mapping for each subject thus attempting to reduce the amount of explicit mapping needed to be made by the user. In order to achieve this the a file containing the list of randomised users is required. This file should have a new row for each _randomisation number_ and _subject id_. In the notebook this is refered to as `randfilename`. Regular expression searches of the column headers define which column is which.

Be aware of this as when output does not behave as expected then this is a good place to start looking. Need to make sure the correct source data points are mapped to the comparison data points.