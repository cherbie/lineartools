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

The config file needs to be in json file requiring 4 key-value pairs to be defined. These are:
 - __FORMS__
 - __VISITS__
 - __FILE__
   - The location of the 
 - __OUTPUT__
   - Location of the output folder. The output _csv_ files will be written to this folder.
