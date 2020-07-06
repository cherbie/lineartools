# Safety Date and Time Reconcilliation
> Ensure vendor comparison file has the same date and times as the _Medrio_ source file.

## Config File Fields

The config file only requires a single field to be defined and that is the **match** field:

- **match** [__REQUIRED__]
  : `Object` containing the visit field that maps every possible exact string visit name to an array index identifier
  - Fields:
    - **visit** [__REQUIRED__]
      : Map all exact string names for visits to an index within the array -> `_array`
      - **\_array** [__REQUIRED__]
        : Array of identifying string names for visits
  - e.g
    ```
    {
      "match": {
        "visit": {
          "Screening": 0,
          "Period 1 Day-2": 1,
          "Period 1 Day 2": 2,
          "Period 2 Day 2": 4,
          "Period 2 Day-2": 3,
          "Period 2 Day 7/EOS": 5,
          "Unscheduled": 6,
          "Day -2 [Period 1]": 1,
          "Day 2 [Period 1]": 2,
          "Day -2 [Period 2]": 3,
          "Day 2 [Period 2]": 4,
          "Day 7 [Period 2] EOS": 5,
          "_array": [
            "Screening",
            "Period 1 Day-2",
            "Period 1 Day 2",
            "Period 2 Day-2",
            "Period 2 Day 2",
            "Period 2 Day 7/EOS",
            "Unscheduled"
          ]
        }
      }
    }
    ```

The sytem avoids the user having to manually specify all the subjects within the study by using the **screening number** in the comparison file and making a _regular expression_ search on the **subject id** column in the source file.
