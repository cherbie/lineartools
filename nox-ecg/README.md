# How to run the application

## Setting up your local environment
The python application has a single third party library dependencies that is needing to be installed prior to execution. This is the __openpyxl__ library that allows for the reading and writing of _.xlsx_ files. Depending on your python package manager this can be installed like so:

__CONDA__

```
$ ~ conda install openpyxl
```

__PIP__

```
$ ~ pip install openpyxl
```

_Note_: The application is dependent on the __Python 3__ distribution and hence will require the __Pip3__ package manager

Prior to execution ensure you have _activated_ your python virtual environment containing the relevant dependencies. This can be performed as so:


__CONDA__

```
$ ~ conda activate [venv_name]
```

_Note_: The virtual environment would need to have been setup prior using the _conda create_ command. See below:

```
$ ~ conda create --name [venv_name]

venv - virtual environment
```

The documentation remains an excellent reference for any issues/difficulties encountered.

__PIP__

Pip required the user to execute an operating system execution environment dependent script that setup's up the python execution environment for the user.

```
MAC OS:
$ ~ source venv/bin/activate

WINDOWS - Command Prompt:
$ ~ .\venv\Scripts\activate.bat

WINDOWS - PowerShell
$ ~ .\venv\Scripts\Activate.ps1
```

_Note_: The virtual environment would need to have been setup prior by running the python module _**venv**_. See below:

```
$ ~ python -m venv venv
```

Directory named _venv_ will be created containing all python virtual environment related files.


## Executing the application
The project folder contains two entry point **_.py_** files that serve two different roles / outcomes.

__Splitting Subjects__

The **_subject\_split.py_** file is responsible for splitting the _.xlsx_ file containing a single worksheet into multiple worksheets on a per subject basis. This is intended to be executed prior to preparing the file for the study team to populate their respective columns. Information needed prior to execution includes:
 - Input _.xlsx_ file containing all collected ECG information
 - Desired output file/path destination
 - A column containing the unique subject identifier for each subject

To execute the python script run the following command:

```
$ ~ python3 subject_split.py
```

The script will prompt the user to input required information through the terminal / standard input stream. Things to be aware of:
 - If any file paths or folders contain spaces, these paths will need to be wrapped in quotation marks.
 - Windows users may need to escape the backslash character used in windows file paths. e.g _".\\\Documents\\\INPUT_FILE.xslx"_

Following the successful execution of the script a new _.xlsx_ file will be create at the specified output path location containing worksheets containing subject specific information.

__Splitting on a per form basis__

The **_form\_split.xlsx_** file is responsible for collecting information from the given _.xlsx_ with worksheets containing information on a per subject basis into _.xlsx_ files based respective __Medrio__ forms. The resulting output files are hence compatible for bulk upload into the subjects stored data.

To execute the python script run the following command.

```
$ ~ python3 form_split.py [filename]

filename - [optional] location/path of the input file
```

The script will prompt the user to input required information through the terminal / standard input stream. Things to be aware of:
 - If any file paths or folders contain spaces, these paths will need to be wrapped in quotation marks.
 - Windows users may need to escape the backslash character used in windows file paths. e.g _".\\\Documents\\\INPUT_FILE.xslx"_

## Jupyter Notebook Execution

Additionally _jupyter notebooks_ have been created for the respective files above that allow for simpler, more visual and increased explanation of the source code's execution plan. These _notebooks_ can optionally be run locally or externally using __Google Colab__ or other free to use or paid computing technologies.

To run the notebook locally the __Jupyter Lab__ python distribution needs to be added to your python execution environment. This can be done like so:

__CONDA__

```
$ ~ conda install -c conda-forge jupyterlab
```

The popular, open-source and well maintained community __conda-forge__ has been used as the distribution channel above to install the __jupyterlab__ distribution.

__PIP__

```
$ ~ pip3 install jupterlab
```

Following the installation, the command __jupyter__ can be used to either open an existing notebook, create a new notebook or the __lab__ can be used to test the execution of python commands using the __IPython__ command shell.

__To open Jupyter Lab__

```
$ ~ jupyter lab
```

__To open Jupter Notebook__

```
$ ~ jupyter notebook
```

These commands will start a local server that allows for browser based editing and rendering. Notebooks can be opened by navigating to the __File__ tab and selecting __Open__ from the drop-down presented.

In-order to execute the __jupyter notebook__ all cells can be run at once by selecting __run-all__ or alternatively each cell can be executed individually sequentially. Please note if an error is encountered or misinformation was entered in previous cells the __kernel will need to be reset__ and the process started again.
