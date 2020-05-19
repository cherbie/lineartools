import re

class ParseData:
    def __init__(self, variables, form_type_map):
        if variables is None or form_type_map is None:
            raise Exception('Process data class \'None\' paramaters')
        self.variables = variables # headers of the input file
        self.typemap: dict = form_type_map
        self.constant_headers_map = {'Subject ID': 2, 'Form Name': 4, 'Group': 1, 'Visit': 3}
        self.data = dict()

    def process_from_config(self, row, formtype: str, ignore_col_before: int):
        '''
        Process row of data using config file specified mapping
        @Return - dict containing all collected data fields
        '''
        assert formtype is not None, 'Error: Formtype is none.' # need to specify the formtype (e.g ECG, Vital Signs etc)
    
        # Get the mapping for formtype in the config file
        typemap = self.typemap.get(formtype, None)
        if typemap is None or typemap.get('_colregex', None) is None:
            print(f"Warning: typemap not identified {formtype}")
            return None
        
        # Get the form variable order
        medrio_order = typemap.get("_medrio_order", None)
        assert medrio_order is not None, "Medrio order must be specified in the config file."
        
        repeat_regex_str = typemap.get("_repregex", None)
        repeat_regex = None
        if repeat_regex_str is None:
            print("Warning: No regular expression defined for repeat.")
        else:
            repeat_regex = re.compile(repeat_regex_str, flags=re.I)
            
        # Ignore Calculated Variables
        calc_regex = re.compile('calc', flags=re.I)
        
        # Get regular expression mapping for medrio variables / headers
        colregex = typemap.get('_colregex', None)
        assert colregex is not None, "Typemap has no column regex / variable regex defined"
        
        # define variable regular expressions to look for matches with
        medrio_order_regex = dict()
        for colname, regex_str in colregex.items():
            medrio_order_regex[colname] = re.compile(regex_str, flags=re.I) # compile all medrio variable searchs (regular expressions)

        # -- PARSE DATA --
        row_data = dict() # dictionary of data
        col = 0 # column index of xlsx cells
        medrio_index = 0 # keep track of form looking order
        searchstr = [None, None]
        for cell in row:
            col += 1 # increment column
            # cycle through all cells in row
            if col < ignore_col_before or cell.value is None or cell.value == '':
                continue # skip empty cell
            
            variable = self.variables[col-1] # medrio variable name
            
            if calc_regex.search(variable) is not None:
                continue # ignore calculated variables
            
            # CYCLE THROUGH ALL POSSIBLE DATA POINTS IN FORM :( ---> this is slow :(
            for colname, regex in medrio_order_regex.items():
                if regex.search(variable) is not None: # mapped to variable (current expected form)
                    # -- LOOK FOR REPEAT --
                    repeat_match = None # keep track of match if repeat
                    
                    if repeat_regex is not None: # config file defines repeats
                        repeat_match = repeat_regex.match(variable) # check if the variable is a repeat variable
                    
                    if repeat_match is not None: # this variable is a repeat
                        colname += f' {repeat_match[0].upper()}' # append repeat identifier to column name
                    
                    # No data overwriting in dictionary
                    assert row_data.get(colname, None) is None, f'Data could be overwritten:\n {row_data}:\n {variable}'
                    
                    # -- Populate Dictionary --
                    if row_data.get(colname, None) is None: # variable has not already been populated
                        medrio_index = (medrio_index + 1)%len(medrio_order) # increment next expected variable
                        row_data[colname] = cell.value # set value data point
                    else: # data point already populated
                        print('Warning: data could be overwritten ... ignored overwrite.')
                    
                    # -- MATCH FOUND --
                    break
                else: # no match found
                    continue
        return row_data
    
    def process_triplicate_from_config(self, row, formtype: str):
        '''
        Need to keep track of what triplicate collection it is.
        The order specified in the config file must match the order variables are seen in the input file!
        '''
        assert formtype is not None, 'Error: Formtype is none.' # need to specify the formtype (e.g ECG, Vital Signs etc)
    
        # Get the mapping for formtype in the config file
        typemap = self.typemap.get(formtype, None)
        if typemap is None or typemap.get('_colregex', None) is None:
            print(f"Warning: typemap not identified {formtype}")
            return None
        
        # Get the form variable order
        medrio_order = typemap.get("_medrio_order", None)
        assert medrio_order is not None, "Medrio order must be specified in the config file."
        
        repeat_regex_str = typemap.get("_repregex", None)
        repeat_regex = None
        if repeat_regex_str is None:
            print("Warning: No regular expression defined for repeat.")
        else:
            repeat_regex = re.compile(repeat_regex_str, flags=re.I)
            
        # Ignore Calculated Variables
        calc_regex = re.compile('calc', flags=re.I)
        
        # Get Triplicate Regex
        trip_regex_str = typemap.get('_triplicateregex', None)
        assert trip_regex_str is not None, 'Config file does not define: "_triplicateregex"'
        trip_regex = re.compile(trip_regex_str, flags=re.I)
        
        # Get regular expression mapping for medrio variables / headers
        colregex = typemap.get('_colregex', None)
        assert colregex is not None, "Typemap has no column regex / variable regex defined"
        
         # define variable regular expressions to look for matches with
        medrio_order_regex = dict()
        for colname, regex_str in colregex.items():
            medrio_order_regex[colname] = re.compile(regex_str, flags=re.I) # compile all medrio variable searchs (regular expressions)

        # -- PARSE DATA --
        row_data = dict() # dictionary of data
        col = 0 # column index of xlsx cells
        medrio_index = 0 # keep track of form looking order
        revolutions = 0
        searchstr = [None, None]
        for cell in row:
            col += 1 # increment column
            # cycle through all cells in row
            if cell.value is None or cell.value == '':
                continue # skip empty cell
            
            variable = self.variables[col-1] # medrio variable name
            
            if calc_regex.search(variable) is not None:
                continue # ignore calculated variables

            # Follow Form Order Of Config File
            curr_colname = medrio_order[medrio_index] # first column expected
            next_colname = medrio_order[(medrio_index+1)%len(medrio_order)] # next column expected
            #print(colname)
            searchstr[0] = colregex.get(curr_colname, None)
            searchstr[1] = colregex.get(next_colname, None)
            #print(searchstr)
            if searchstr is None: # no regex match
                continue
            if re.search(searchstr[0], variable, flags=re.I) is not None: # mapped to variable (current expected form)
                
                repeat_match = None # keep track of match if repeat
                if repeat_regex is not None: # could be repeats
                    repeat_match = repeat_regex.match(variable) # check if the variable is a repeat variable
                if repeat_match is not None: # this variable is a repeat
                    curr_colname += f' {repeat_match[0].upper()}' # append repeat identifier to column name
                    revolutions = 0 # reset triplicate count
                    
                #assert row_data.get(curr_colname, None) is None, f'Data could be overwritten:\n {row_data}:\n {variable}'
                
                # -- Populate Dictionary --
                if row_data.get(curr_colname, None) is None: # variable has not already been populated
                    curr_colname += f' [#{revolutions}]'
                    medrio_index = (medrio_index + 1)%len(medrio_order) # increment next expected variable
                    if medrio_index == 0: # about to make a revolution
                        revolutions += 1 # increment triplicate count
                    row_data[curr_colname] = cell.value # set value data point
                else: # data point already populated
                    print('Warning: data could be overwritten ... overwrite ignored')
                    print(f'{row_data}\n{curr_colname}')
            
            elif re.search(searchstr[1], variable, flags=re.I) is not None: # mapped to variable (next expected form)
                
                repeat_match = None # keep track of match if repeat
                if repeat_regex is not None: # could be repeats
                    repeat_match = repeat_regex.match(variable) # check if the variable is a repeat variable
                if repeat_match is not None: # this variable is a repeat
                    next_colname += f' {repeat_match[0].upper()}' # append repeat identifier to column name
                    revolutions = 0 # reset triplicate tracker
                    
                # assert row_data.get(next_colname, None) is None, f'Data could be overwritten:\n {row_data}:\n {variable}'
                
                # -- Populate Dictionary --
                if row_data.get(next_colname, None) is None: # variable has not already been populated
                    next_colname += f' [#{revolutions}]'
                    medrio_index = (medrio_index + 2)%len(medrio_order) # increment past next expected data point
                    if ((medrio_index+1)%len(medrio_order)) == (len(medrio_order) - 1): # about to make a revolution
                        revolutions += 1 # increment triplicate count
                    row_data[next_colname] = cell.value # set value data point
                else: # data point already populated
                    print('Warning: data could be overwritten ... overwrite ignored')
                    print(f'{row_data}\n{next_colname}')

        return row_data
    
    def process_generalised_cells(self, row):
        '''
        Process the column headers that are constant
        '''
        row_dict = dict()
        for header, row_index in self.constant_headers_map.items():
            row_dict[header] = row[row_index].value # extract value of cell
        return row_dict;
        
    def add_row(self, row, tabname='Errors'):
        if row is None:
            return
        
        if self.data.get(tabname, None) is None:
            self.data[tabname] = list() # create iterable list
        
        self.data.get(tabname, None).append(row)
        
        '''
        Could do dictionary key difference checking
        '''
        return

    def get_data(self):
        return self.data or None    
        
    def generate_form_type(self, formname=None):
        '''
        Generate the identifier for the form (group the forms for output)
        
        @Returns - None if not type map could be made.
        '''
        if formname is None:
            raise Exception('Formname cannot be None')
        formtype = None # form type identifier
        triplicate = False
        for t, typemap in self.typemap.items():
            # print(t)
            if typemap.get('_formregex', None) is not None and re.search(typemap.get('_formregex', None), formname, flags=re.I) is not None: # there was a match
                formtype = t
                if typemap.get('_triplicateregex', None) is not None and re.search(typemap.get('_triplicateregex', None), formname, flags=re.I) is not None:
                    triplicate = True
                break
            
        return (formtype, triplicate)