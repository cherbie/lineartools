# Study Summary Report Generator
> __Author__: _@clayton-herbst_

## Setting Up The Local Environment
This package uses the __[Conda](https://docs.conda.io)__ python package manager. In order to set up your _python_ execution environment, set up a new _conda_ environment using the `environment.yml` file in the home directory.

```
% ~ conda env create -f=/path/to/environment.yml -n env_name
```

In order to enter/activate the newly created _conda_ environment execute the following command:

```
% ~ conda activate env_name
```

See the __conda__ [docs](https://docs.conda.io) for further details.

## Running Jupyter Notebooks
The application has been designed to be executed within _[Jupyter Notebooks](https://jupyter.org/)_, a handy graphical tool that allows for execution of python applications on the web.

The major benefit of __Jupyter Notebooks__ in this application has been the enhanced documentation and visual aspect to code blocks. _Markdown_ cells accompany _python code_ cells in order to better explain the application flow. Any source code that is not at the surface level of this process flow has been abstracted away in the `./src/*` directory.

In order to run the __Jupyter notebook__ execute the following command:

```
(conda_env) $ ~ jupyter notebook
```

and then select the `./*.ipynb` file. Read the __Jupyter Notebooks__ getting started guide, however the __Kernel__ tab is a great place to note for quick and easy execution of the entire file. 

Note it is expected certain variable values within the file will need to be updated on a per execution basis such as:
 - input file path location
 - output directory path location

Output for code blocks such as the configuration file parser is provided as an in-execution of parsed values.

## Config File Unpacked
The config file is a `json` file created by the application user in order to direct the program flow and assist the program in recongnising complicated relationships. This feature has allowed for the generalisation of the process. In most use cases the `./template_config.json` file provided will be most a handy start.

__Json__ files can be read about in more detail using the web however they are essentially a large object consisting of _key-value_ pairs.

### Config Key-Value Pair Structure

```
{
  tabs: String[],
  general_headers: String[],
  map: {
    formtype: objectOf(form_map)
  }
}
```

### Config Key's

__tab__
  : Tab headers to feature in output file as the title of the workbook tabs.
  - Consists of an array of form name's / form types needed in the output file.
  - Need to have a respective key-map in the __map__ config
  - e.g `["Triplicate ECG", "Adverse Events"]`

__general_headers__
  : Identical string matches to the input file column headers that are generic to all rows. [`CASE_SENSITIVE`]
  - e.g `["Medrio ID", "Subject ID", "Form", "Visit"]`

__map__
  : Object containing key value mappings to __form_map__ objects from __tab__ names.
  - Map's not specified for particular form's will cause the form to be skipped by the program.

__form_map__
  : Object containing a number of `REQUIRED` and `OPTIONAL` fields based on desired program execution flow.
  - `REQUIRED` Fields:
    - __\_formregex__
      : The _regex_ string used to identify the form from the 
      form name.
      - type: String

    - __\_colregex__
      :  Object containing key's of data points and the _regex_ string used to identify these data points from variable names.
      - type: Object
      - See `./template_config.json` for examples
  - `OPTIONAL` Fields
    : Fields that provide extended functionality to the program flow.
    - __\_variable\_headers
      : Object that allows for complicated data _re-structuring_ and _formatting_ by specifying attributes and cell content bahaviour.
    - type: Object
    - __key__
      : must map exactly to string specified in _\_colregex_.
      - The header of data point will default to the data captured by the key.
      - e.g physical exam "System" data point in the header column names.
    - __value__ fields
      : Object controlling behaviour of data point 
      - __content__
        : an exact string reference to data point defined in *\_colregex*
        - The cell contents will consist of contents of referenced data point
      - __header\_ref__
        : an exact string reference to a data point defined in *\_colregex*
        - Reference data is concatenated to header satisfying need for unique headers and allowing for distinguishable data.
      - __\_concatenate__
        : string that is blindy concatenated to the end of the header.
      - __\_increment__
        : If specified as true will randomly increment the header.
    - __\_triplicateregex__
      : Regex string that allows for matches the form name when a triplicate search is required.
      - If not specified the system will not be aware of triplicate collections and may overwrite the first collection data.
    - __\_triplicate\_id\_regex__
      : Regex string that allows for matches and identification of the particular order of data point collection from the _variable name_.
      - Need to use _regex_ capturing groups to allow for only number identification. e.g (_#2 -> 2)
    - __repregex__
      : Regex string that allows for matches and identification of the particular repeat order referenced within the _variable name_
      - Use of capturing group will assist in beautifying headers generated by output file.
      - If not specified the system will not be aware of repeat collections and may overwrite the first collection data.