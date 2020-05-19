import os
from openpyxl import Workbook

class FileWriter:
    def __init__(self, dirname: str, name: str, tabs: list, dictionary_data: dict):
        if not os.path.exists(dirname):
            print(f'Creating Directory: {dirname}')
            os.mkdir(dirname)
        self.filename = f'{dirname}/{name}.xlsx'
        self.tabs = tabs
        self.wb = Workbook(write_only=True) # create new workbook
        self.data = dictionary_data # all parsed data
        self.baseheaders = ['Subject ID', 'Form Name', 'Group', 'Visit']
        

    def find_headers(self, tab: str):
        '''
        @param fieldnames - iterable list of fieldnames
        '''
        assert self.data.get(tab, None) is not None, "Error: Tab is not defined in parsed data dictionary. Check config file!"
        
        headers_dict = dict.fromkeys(self.baseheaders)
        for data in self.data.get(tab, None):
            headers_dict.update(data) # add keys to list
    
        headers = list(headers_dict.keys())
        
        
        return headers

    def write_worksheet(self, tab: str):
        '''
        @Return - all document headers
        '''
        ws = self.wb.create_sheet()
        ws.title = tab
        
        datapoints = self.data.get(tab, None)
        
        if datapoints is None:
            return # no data
        
        # -- Write Headers --
        columns = self.find_headers(tab)
        headers = list()
        for i in columns:
            headers.append(i.capitalize())
        ws.append(headers)
        
        # -- Write Content --
        for data in datapoints:
            row = list()
            for col in columns:
                row.append(data.get(col, None)) # add data to row
            ws.append(row) # write to file
        
        return

    def getFilename(self):
        return self.filename

    def close(self):
        '''
        Saves the excel file to file and then closes the file properly.
        '''
        return self.wb.save(self.filename)