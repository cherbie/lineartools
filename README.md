# Noxopharm ECG Upload
Python script to automate the excel file build process for Noxopharm ECG uploads.

## Instructions
The entry point to the script is the _app.py_ file in the _project_ folder. In order to run the file ensure your python environment is configured using the _requirements.txt_ file. This can be done so using __pip3__:

```
 ~ pip3 install -r requirements.txt
```

The script can be run like so:

```
 ~ python3 app.py (config)

 config - the location of the config file
```

The config file needs to be in json file format (__*.json__), requiring 4 key-value pairs to be defined. These are:
 - __FORMS__
   - Array of strings, listing the names of all applicable study forms for which data needs to be uploaded for.
   - Exact string match is __important__
 - __VISITS__
   - Array of strings, listing all applicable visits within the study
   - Exact string match is __critical__.
 - __FILE__
   - The location of the ECG data source file (.xlsx file format)
 - __OUTPUT__
   - Location of the output folder. The output _.csv_/_.xlsx_ files will be written to this folder.

```
e.g config.json

{
    "FORMS": ["12 Lead ECG (Triplicate)", "Unscheduled 12-Lead Triplicate ECG", "45MIN Predose 12 Lead ECG (Triplicate)",
        "30MIN Predose 12 Lead ECG (Triplicate)", "15MIN Predose 12 Lead ECG (Triplicate)", "30MIN 12 Lead ECG (Triplicate)",
        "1HR 12 Lead ECG (Triplicate)", "1.5HR 12 Lead ECG (Triplicate)", "2HR 12 Lead ECG (Triplicate)", "3HR 12 Lead ECG (Triplicate)",
        "4HR 12 Lead ECG (Triplicate)", "5HR 12 Lead ECG (Triplicate)", "6HR 12 Lead ECG (Triplicate)", "8HR 12 Lead ECG (Triplicate)",
        "12HR 12 Lead ECG (Triplicate)", "16HR 12 Lead ECG (Triplicate)", "24HR 12 Lead ECG (Triplicate)", "48HR 12 Lead ECG (Triplicate)",
        "72HR 12 Lead ECG (Triplicate)", "144HR 12 Lead ECG (Triplicate)"],
    "VISITS": ["Screening", "Day -2 [Period 1]", "Day -1 [Period 1]", "Day 1 [Period 1]", "Day 2 [Period 1]", "Day 3 [Period 1]",
        "Day 4 [Period 1]", "Day -2 [Period 2]", "Day -1 [Period 2]", "Day 1 [Period 2]", "Day 2 [Period 2]", "Day 3 [Period 2]", 
        "Day 4 [Period 2]", "Day 7 [Period 2]  EOS", "Unscheduled Visits"],
    "FILE": "/Users/herbsca/OneDrive/development/nox-ecg/project/test/input/NOX_TEMPLATE.xlsx",
    "OUTPUT": "/Users/herbsca/OneDrive/development/nox-ecg/project/test/output"
}
```

