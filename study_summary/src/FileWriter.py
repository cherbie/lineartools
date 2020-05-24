import os
from openpyxl import Workbook

'''
Class responsible for the writing of the output xlsx file
'''
class FileWriter:

    '''
    @param dirname - name of the output directory
    @param name - file name to be placed within the output directory
    @param tabs - list of tabs to be included in output xlsx file
    @param dictionary_data - formatted data to be used to write to file
    '''
    def __init__(self, dirname: str, name: str, tabs: list, dictionary_data: dict):
        if not os.path.exists(dirname):
            print(f'Creating Directory: {dirname}')
            os.mkdir(dirname)
        self.filename = f'{dirname}/{name}.xlsx'
        self.tabs = tabs
        self.wb = Workbook(write_only=True) # optimised for large file writing
        self.data = dictionary_data # all parsed data
        self.baseheaders = ['Subject ID', 'Form Name', 'Group', 'Visit']
        
    '''
    Find all column headers for a particular output .xlsx file tab.
    @Param fieldnames - iterable list of fieldnames
    @Return headers: list - list of all column headers for the document
    '''
    def find_headers(self, tab: str):
        
        assert self.data.get(tab, None) is not None, f"Error: {tab} is not defined in parsed data dictionary. Check config file!"
        
        # -- Add base headers to columns
        headers_dict = dict.fromkeys(self.baseheaders)

        # -- Cycle through parsed data adding new column headers as found
        for data in self.data.get(tab, None):
            headers_dict.update(data) # add keys to list
    
        # -- Extract all headers -- keys of the dictionary created
        return list(headers_dict.keys())
    '''
    Cycle through all parsed data for a particular tab and write to output .xlsx file the data.
    @Param tab: str - the tab to cycle through
    @Return - all tab headers
    '''
    def write_worksheet(self, tab: str):
        ws = self.wb.create_sheet()
        ws.title = tab
        
        datapoints = self.data.get(tab, None)
        
        if datapoints is None:
            return # no data
        
        # -- Write Headers --
        # -- Find list of column headers to write
        columns = self.find_headers(tab)

        # -- Format the column headers
        headers = list()
        for i in columns:
            headers.append(i.capitalize())

        # -- Write headers to first row
        ws.append(headers)
        
        # -- Write parsed data to rows
        for data in datapoints:
            # -- Cycle through each column header and add data if it exists
            row = list()
            for col in columns:
                row.append(data.get(col, None)) # add data to row
            ws.append(row) # write to file
        
        return headers

    '''
    @Return filename: str -- file path of the output file
    '''
    def getFilename(self):
        return self.filename

    '''
    Saves and actually writes the excel file to file and then closes the file properly.
    @Required
    '''
    def close(self):
        return self.wb.save(self.filename)