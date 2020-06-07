import re


'''
Class responsible for managing state of parsed data and applying data re-structuring
'''
class ParseData:
    '''
    @Param variables: list -- column headers of the input file
    @Param form_type_map: dict -- config file form-type mapping for variables to data point
    '''
    def __init__(self, variables, form_type_map, general_headers):
        if variables is None or form_type_map is None:
            raise Exception('ParseData constructor contains \'None\' paramaters')
        self.variables: list = variables # headers of the input file
        self.typemap: dict = form_type_map
        self.constant_headers_map = ParseData.setHeadersMap(general_headers)
        self.data = dict()
    
    def setHeadersMap(headers: list):
        map = dict()
        for itx, header in enumerate(headers):
            map[header] = itx
        return map

    '''
    Process row of data using config file specified mapping for forms that do not contain triplicate data points.

    @Param row - openpyxl row of cells to process
    @Param formtype: str - the tab name / form-type to process
    @Param ignore_col_before: int - the column index at which each row becomes unique (i.e not standardised headers)

    @Return - dict containing all collected data fields or None on error
    '''
    def process_from_config(self, row, formtype: str, ignore_col_before: int, start_dict: dict = dict(), err_logger = None):
        assert formtype is not None, 'Error: Formtype is None.' # need to specify the formtype (e.g ECG, Vital Signs etc)
        assert row is not None, 'Error: openpyxl row is None'
    
        # -- Get the mapping for formtype in the config file
        typemap = self.typemap.get(formtype, None)
        if typemap is None or typemap.get('_colregex', None) is None:
            error = {
                "type": "WARNING",
                "message": f"Error: typemap not identified {formtype}",
                "function": "ParseData.process_from_config"
            }
            if err_logger is not None:
                err_logger.add({**start_dict, **error})
            else:
                print(f"Error: typemap not identified {formtype}")
            return None
        
        # -- Get the form variable order
        medrio_order = typemap.get("_medrio_order", None)
        assert medrio_order is not None, "Medrio order must be specified in the config file. (\'_medrio_order\')"
        
        # -- Find if repeat's need to be identified 
        repeat_regex_str = typemap.get("_repregex", None)
        repeat_regex = None
        if repeat_regex_str is not None: # need to 
            repeat_regex = re.compile(repeat_regex_str, flags=re.I)
            
        # -- Ignore calculated variables
        calc_regex = re.compile('calc', flags=re.I)
        
        # -- Get regular expression mapping for medrio variables / headers
        colregex = typemap.get('_colregex', None)
        assert colregex is not None, "Typemap has no column regex / variable regex defined"
        
        # -- Define variable regular expressions objects
        medrio_order_regex = dict()
        for colname, regex_str in colregex.items():
            medrio_order_regex[colname] = re.compile(regex_str, flags=re.I) # compile all medrio variable searchs (regular expressions)

        # -- PARSE DATA --
        row_data = start_dict # dictionary of data
        col = 0 # column index of xlsx cells
        medrio_index = 0 # keep track of form looking order
        searchstr = [None, None]

        # -- Cycle through all cells in row
        for cell in row:
            col += 1 # increment column index

            # -- Skip empty cells or generic cells
            if col < ignore_col_before or cell.value is None or cell.value == '':
                continue # skip empty cell
            
            # -- Get medrio variable name
            variable = self.variables[col-1]
            
            # -- Ignore calculated variables
            if calc_regex.search(variable) is not None:
                continue
            
            # -- Cycle through all possible variable mappings (config file specified)
            for colname, regex in medrio_order_regex.items():
                # -- Variable is mapped to config file data points
                if regex.search(variable) is not None: # mapped to variable (current expected form)
                    # -- LOOK FOR REPEAT --
                    repeat_match = None # keep track of match if repeat
                    if repeat_regex is not None: # config file defines repeats
                        repeat_match = repeat_regex.search(variable) # check if the variable is a repeat variable
                    
                    # -- Concat repeat value
                    if repeat_match is not None: # this variable is a repeat
                        colname += f' [{repeat_match.group(1).upper()}]' # append repeat identifier to column name
                    
                    # -- Populate Dictionary --
                    if row_data.get(colname, None) is None: # variable has not already been populated
                        medrio_index = (medrio_index + 1)%len(medrio_order) # increment next expected variable
                        row_data[colname] = cell.value # set value data point
                    else: # data point already populated
                        error = {
                            "type": "ERROR",
                            "message": f"Warning: data could be overwritten ... ignored overwrite.\n{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}",
                            "function": "ParseData.process_from_config"
                        }
                        if err_logger is not None:
                            err_logger.add({**start_dict, **error})
                        else:
                            print(' -----    Warning: data could be overwritten ... ignored overwrite. ------ ')
                            print(f'{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}')
                    
                    # -- MATCH FOUND --
                    break
                else:
                    # -- No match found
                    continue
        return row_data
    
    '''
    Process row of data using config file specified mapping for forms that contain triplicate data points.
    Keeps track of cycles through medrio_order and thus can label triplicates.

    @Param row - openpyxl row of cells to process
    @Param formtype: str - the tab name / form-type to process
    @Param ignore_col_before: int - the column index at which each row becomes unique (i.e not standardised headers)

    @Return - dict containing all collected data fields or None on error
    '''
    def process_triplicate_order(self, row, formtype: str, ignore_col_before: int, start_dict: dict = dict(), err_logger = None):

        assert formtype is not None, 'Error: Formtype is None.'
        assert row is not None, 'Error, Row paramater is None'
    
        # -- Get the mapping for formtype in the config file
        typemap = self.typemap.get(formtype, None)
        if typemap is None or typemap.get('_colregex', None) is None:
            error = {
                "type": "WARNING",
                "message": f"Warning: Typemap not identified for {formtype}.\nCheck config file.",
                "function": "ParseData.process_triplicate_from_config"
            }
            if err_logger is not None:
                err_logger.add({**start_dict, **error})
            else:
                print(f"Warning: Typemap not identified for {formtype}.\nCheck config file.")
            return None
        
        # -- Get the form variable order
        medrio_order = typemap.get("_medrio_order", None)
        assert medrio_order is not None, "Medrio order must be specified in the config file."
        
        # -- Check if repeat's need to be defined
        repeat_regex_str = typemap.get("_repregex", None)
        repeat_regex = None
        if repeat_regex_str is not None:
            repeat_regex = re.compile(repeat_regex_str, flags=re.I)
            
        # -- Ignore Calculated Variables
        calc_regex = re.compile('calc', flags=re.I)
        
        # -- Get Triplicate Regex
        trip_regex_str = typemap.get('_triplicateregex', None)
        assert trip_regex_str is not None, 'Config file does not define: \'_triplicateregex\' for {formtype}'
        trip_regex = re.compile(trip_regex_str, flags=re.I)
        
        # -- Get regular expression mapping for medrio variables / headers
        colregex = typemap.get('_colregex', None)
        assert colregex is not None, "Typemap has no column regex / variable regex defined in config file"
        
         # -- Define variable regular expressions to look for matches with
        medrio_order_regex = dict()
        for colname, regex_str in colregex.items():
            medrio_order_regex[colname] = re.compile(regex_str, flags=re.I) # compile all medrio variable searchs (regular expressions)

        # -- PARSE DATA --
        row_data = start_dict # dictionary of data
        col = 0 # column index of xlsx cells
        medrio_index = 0 # keep track of form looking order
        revolutions = 0
        searchstr = [None, None]

        # -- Cycle through each column / cell in row
        for cell in row:
            col += 1 # increment column
            
            # -- Skip empty cells or generic cells
            if col < ignore_col_before or cell.value is None or cell.value == '':
                continue # skip empty cell
            
            # -- Fetch medrio variable name
            variable = self.variables[col-1]

            # -- Ignore calculated variables
            if calc_regex.search(variable) is not None:
                continue

            # -- Follow form order provided by medrio_order
            curr_colname = medrio_order[medrio_index] # first column expected
            next_colname = medrio_order[(medrio_index+1)%len(medrio_order)] # next column expected
            searchstr[0] = colregex.get(curr_colname, None)
            searchstr[1] = colregex.get(next_colname, None)
            # -- Not regex defined
            if searchstr[0] is None or searchstr[1] is None:
                continue
            
            # -- Mapping variable to search string
            if re.search(searchstr[0], variable, flags=re.I) is not None: # mapped to variable (current expected form)
                repeat_match = None # keep track of match if repeat
                if repeat_regex is not None: # could be repeats
                    repeat_match = repeat_regex.search(variable) # check if the variable is a repeat variable
                
                # -- Repeat match -> hence variable is repeat
                if repeat_match is not None: # this variable is a repeat
                    curr_colname += f' [{repeat_match[0].upper()}]' # append repeat identifier to column name
                    #revolutions = 0 # reset triplicate count
                                    
                # -- Populate Dictionary --
                if row_data.get(curr_colname, None) is None: # variable has not already been populated
                    curr_colname += f' [#{revolutions}]'
                    medrio_index = (medrio_index + 1)%len(medrio_order) # increment next expected variable
                    if medrio_index == 0: # about to make a revolution
                        revolutions += 1 # increment triplicate count
                    row_data[curr_colname] = cell.value # set value data point
                else: # data point already populated
                    error = {
                        "type": "ERROR",
                        "message": f"WARNING: data could be overwritten ... ignored overwrite.\n{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}",
                        "function": "ParseData.process_triplicate_from_config"
                    }
                    if err_logger is not None:
                        err_logger.add({**start_dict, **error})
                    else:
                        print(' -----    Warning: data could be overwritten ... ignored overwrite. ------ ')
                        print(f'{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}')
            
            # -- Search for next column incase variable was skipped
            elif re.search(searchstr[1], variable, flags=re.I) is not None: # mapped to variable (next expected form)
                repeat_match = None # keep track of match if repeat
                if repeat_regex is not None: # could be repeats
                    repeat_match = repeat_regex.search(variable) # check if the variable is a repeat variable

                # -- Repeat match found
                if repeat_match is not None: # this variable is a repeat
                    next_colname += f' [{repeat_match.group(1).upper()}]' # append repeat identifier to column name
                    # revolutions = 0 # reset triplicate tracker
                    
                # -- Populate Dictionary --
                if row_data.get(next_colname, None) is None: # variable has not already been populated
                    next_colname += f' [#{revolutions}]'
                    medrio_index = (medrio_index + 2)%len(medrio_order) # increment past next expected data point
                    if ((medrio_index+1)%len(medrio_order)) == (len(medrio_order) - 1): # about to make a revolution
                        revolutions += 1 # increment triplicate count
                    row_data[next_colname] = cell.value # set value data point
                else: # data point already populated
                    error = {
                        "type": "ERROR",
                        "message": f"WARNING: data could be overwritten ... ignored overwrite.\n{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}",
                        "function": "ParseData.process_triplicate_from_config"
                    }
                    if err_logger is not None:
                        err_logger.add({**start_dict, **error})
                    else:
                        print(' -----    ERROR: data could be overwritten ... ignored overwrite. ------ ')
                        print(f'{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}')

        return row_data
    
    '''
    Process row of data using config file specified mapping for forms that contain triplicate data points.
    Keeps track of cycles through medrio_order and thus can label triplicates.

    @Param row - openpyxl row of cells to process
    @Param formtype: str - the tab name / form-type to process
    @Param ignore_col_before: int - the column index at which each row becomes unique (i.e not standardised headers)

    @Return - dict containing all collected data fields or None on error
    '''
    def process_triplicate_loop(self, row, formtype: str, ignore_col_before: int, start_dict: dict = dict(), err_logger = None):

        assert formtype is not None, 'Error: Formtype is None.'
        assert row is not None, 'Error, Row paramater is None'
    
        # -- Get the mapping for formtype in the config file
        typemap = self.typemap.get(formtype, None)
        if typemap is None or typemap.get('_colregex', None) is None:
            error = {
                "type": "WARNING",
                "message": f"Warning: Typemap not identified for {formtype}.\nCheck config file.",
                "function": "ParseData.process_triplicate_from_config"
            }
            if err_logger is not None:
                err_logger.add({**start_dict, **error})
            else:
                print(f"Warning: Typemap not identified for {formtype}.\nCheck config file.")
            return None
        
        # -- Get the regex identifier for the order
        triplicate_id_regex_str = typemap.get("_triplicate_id_regex", None)
        assert triplicate_id_regex_str is not None, "function 'process_triplicate_loop' needs '_triplicate_id_regex' to be defined in the config file"
        triplicate_id_regex = re.compile(triplicate_id_regex_str)
        
        # -- Get the form variable order
        #medrio_order = typemap.get("_medrio_order", None)
        #assert medrio_order is not None, "Medrio order must be specified in the config file."
        
        # -- Check if repeat's need to be defined
        repeat_regex_str = typemap.get("_repregex", None)
        repeat_regex = None
        if repeat_regex_str is not None:
            repeat_regex = re.compile(repeat_regex_str, flags=re.I)
            
        # -- Ignore Calculated Variables
        calc_regex = re.compile('calc', flags=re.I)
        
        # -- Get regular expression mapping for medrio variables / headers
        colregex = typemap.get('_colregex', None)
        assert colregex is not None, "Typemap has no column regex / variable regex defined in config file"
        
         # -- Define variable regular expressions to look for matches with
        medrio_order_regex = dict()
        for colname, col_regex_str in colregex.items():
            medrio_order_regex[colname] = re.compile(col_regex_str, flags=re.I) # compile all medrio variable searchs (regular expressions)

        # -- PARSE DATA --
        row_data = start_dict # dictionary of data
        col = 0 # column index of xlsx cells
        # medrio_index = 0 # keep track of next expected value for weak error handleing
        revolutions = 1 # keep track of current repeat for weak error handling
        searchstr = [None, None]

        # -- Cycle through each column / cell in row
        for cell in row:
            col += 1 # increment column
            
            # -- Skip empty cells or generic cells
            if col < ignore_col_before or cell.value is None or cell.value == '':
                continue # skip empty cell
            
            # -- Fetch medrio variable name
            variable = self.variables[col-1]

            # -- Ignore calculated variables
            if calc_regex.search(variable) is not None:
                continue
            
            # ----

            # -- Cycle through all possible variable mappings (config file specified)
            for colname, regex in medrio_order_regex.items():
                # -- Variable is mapped to config file data points
                if regex.search(variable) is not None: # mapped to variable (current expected form)
                    # -- LOOK FOR REPEAT --
                    repeat_match = None # keep track of match if repeat
                    if repeat_regex is not None: # config file defines repeats
                        repeat_match = repeat_regex.search(variable) # check if the variable is a repeat variable
                    
                    # -- LOOK FOR TRIPLICATE ID --
                    triplicate_id_match = triplicate_id_regex.search(variable) # keep track of match if id found

                    # -- CONCAT TRIPLICATE ID TO COLUMN NAME
                    if(triplicate_id_match is not None): # match
                        colname += f' [#{triplicate_id_match.group(1)}]'
                        revolutions = triplicate_id_match.group(1)
                    else:
                        colname += f' [#{revolutions}]' # weak error handling (assume the most likely repeat id)
                        # Log warning
                        error = {
                            "type": "ERROR",
                            "message": f"Warning: Could not identify triplicate id (triplicate_id_regex in config). Data could be overwritten as a result. Program continued using '{colname}' as the column identifier.\n{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}",
                            "function": "ParseData.process_triplicate_loop"
                        }
                        if err_logger is not None:
                            err_logger.add({**start_dict, **error})
                        else: # logger not defined
                            print(' -----    Warning: data could be overwritten ... ignored overwrite. ------ ')
                            print(f'{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}')
                    
                    # -- Concat repeat value
                    if repeat_match is not None: # this variable is a repeat
                        colname += f' [{repeat_match.group(0).upper()}]' # append repeat identifier to column name
                    
                    # -- Populate dictionary --
                    if row_data.get(colname, None) is None: # variable has not already been populated
                        #medrio_index = (medrio_index + 1)%len(medrio_order) # increment next expected variable
                        row_data[colname] = cell.value # set value data point
                    else: # data point already populated
                        error = {
                            "type": "ERROR",
                            "message": f"Warning: data could be overwritten ... ignored overwrite.\n{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}",
                            "function": "ParseData.process_from_config"
                        }
                        if err_logger is not None:
                            err_logger.add({**start_dict, **error})
                        else:
                            print(' -----    Warning: data could be overwritten ... ignored overwrite. ------ ')
                            print(f'{formtype}\n{row_data}\n{colname}: {cell.value}\n{variable}')
                    
                    # -- MATCH FOUND --
                    break
                else:
                    # -- No match found
                    continue
            # ---
        return row_data

    '''
    Responsible for formating the data prior to printing to output
    '''
    def format_data(self, err_logger = None):
        # -- Define generic headers
        identifying_headers = ['Subject ID', 'Form Name', 'Group', 'Visit']

        # -- Cycle through each form type looking for formating declarations
        for formtype, typemap in self.typemap.items():
            variable_headers_map = typemap.get("_variable_headers", None)
            variable_spread_map = typemap.get("_spread_variable", None)
            
            # -- Check if formating declarations are made in form
            if variable_headers_map is None and variable_spread_map is None: # checks to see the _variable_headers subdocument is defined in the config file
                continue
            
            # -- These forms need to have their data re-arrranged
            data_old = self.data.get(formtype, None);
            if data_old is None:
                continue # data is not defined

            # -- Restructing old form data            
            data_new = dict()
            inc = 0 # keep track of unique increment
            for data in data_old:
                id = '' # empty
                inc += 1

                # -- Cycle through all generic identifying headers in input file
                for subid in identifying_headers:
                    id += data.get(subid, '') # concat to create id
                
                # -- No data exists yet so populate with general data
                if data_new.get(id, None) is None:
                    data_new[id] = {**data}
                else:
                    data_new[id].update(data) # merge rows of data
                
                # -- Cycle through all header rearrangements specified in config file
                if variable_headers_map is not None:

                    # -- Handle the compression of headers
                    row_id = 0
                    for location_name, location_map in variable_headers_map.items(): #
                        row_id += 1
                        inc += 1
                        cell_contents_name = location_map.get('content', '') # the name of the data point to include as the cell contents
                        header = location_map.get("header_exact", None) # the base header of new column
                        header_ref_string= location_map.get("header_ref", None)  # the variable reference to be used in header
                        header_ref = data.get(header_ref_string, None)
                        cell_header = data.get(location_name, None)
                        increment = location_map.get("_increment", False) # increment
                        concat = location_map.get("_concatenate", None)

                        # -- header_exact & header_ref are defined --> concatenate header ref to header
                        if header is not None and header_ref is not None:
                            header += f" [{header_ref}]"
                        elif header_ref is not None: # header_exact is not defined
                            header = header_ref
                        elif header is None: # header is equal to the value of a cell
                            header = cell_header

                        # -- Check if header remains none
                        if header is None: # header cannot be determined
                            error = {
                                "type": "WARNING",
                                "message": "Warning: Header is not defined in config file (formatting).",
                                "function": "ParseData.format_data"
                            }
                            if err_logger is not None:
                                err_logger.add({**data, **error})
                            else:
                                print("Warning: Header is not defined in config file (formatting).")
                            
                            # Skip
                            continue
                            
                        
                        # -- Increment header --> specified in config file ("_increment")
                        if increment:
                            header += f' -{inc}'
                        
                        # -- Concatenate string to header --> specified in config file ("_concatenate")
                        if concat is not None:
                            header += f"{concat}"
                        
                        # -- Delete exisiting header and create new header
                        if data_new[id].get(location_name, None) is not None:
                            del data_new[id][location_name] # delete the existing header
                        if data_new[id].get(cell_contents_name, None) is not None:
                            del data_new[id][cell_contents_name] # delete the contents of the new header
                        data_new[id][header] = f'{data.get(cell_contents_name, "")}' # populate cell contents

            # -- Repopulate the global dictionary
            data_list = list()
            for id, data in data_new.items():
                data_list.append(data) # create row's of data
            
            # -- Redefine object context
            self.data[formtype] = data_list
    
    '''
    Process the column headers that are constant

    @Param row -- row of data

    @Return row_dict: dict -- dictionary containing generic headers and their contents
    '''
    def process_generalised_cells(self, row):
        row_dict = dict()
        for header, row_index in self.constant_headers_map.items():
            row_dict[header] = row[row_index].value # extract value of cell
        return row_dict;
        
    '''
    Add row of data to a particular formtype

    @Param row - openpyxl data cells
    @Param tabname: str - formtype / tabname
    '''
    def add_row(self, row, tabname:str ='Errors'):
        # Row needs to have data
        assert row is not None, "Row data needs to be defined"
        assert tabname is not None, "Tabname/formtype needs to be defined"
        
        # -- Data has not been defined for tabname/formtype
        if self.data.get(tabname, None) is None:
            self.data[tabname] = list() # create iterable list

        # -- Append data to list    
        self.data.get(tabname, None).append(row)
        
        '''
        @feature - Could do dictionary key difference checking
        '''
        return None

    '''
    Accessor method for current state of data
    '''
    def get_data(self):
        return self.data or None 
    
    '''
    Generate the identifier for the form (group the forms for output)

    @Returns (formtype, istriplicate, typemap): tuple - describing the form identifier and whether the form is a triplicate or not 
    '''
    def generate_form_type(self, formname=None):
        assert formname is not None, f'Formname cannot be None.'

        formtype = None # form type identifier
        triplicate = False
        form_typemap = None
        for t, typemap in self.typemap.items():
            # print(t)
            if typemap.get('_formregex', None) is not None and re.search(typemap.get('_formregex', None), formname, flags=re.I) is not None: # there was a match
                formtype = t
                if typemap.get('_triplicateregex', None) is not None and re.search(typemap.get('_triplicateregex', None), formname, flags=re.I) is not None:
                    triplicate = True
                form_typemap = typemap
                break
            
        return (formtype, triplicate, form_typemap)