import sys

class FileWriter:
    def __init__(self, name, fieldnames):
        self.filename = f'{name}.csv'
        self.file = open(self.filename, 'wb')
        self.headers = fieldnames
        self.writer = csv.DictWriter(self.file, fieldnames=fieldnames, restval='', delimiter=',')
        self.writer.writeHeader()
    
    def bulkWrite(self, entries):
        '''
        @param entries array of dictionary entries
        '''
        self.writer.writerows(entries)
        return
    
    def singleWrite(self, entry):
        '''
        @param entry - dictionary entry
        '''
        self.writer.writerow(entry)
    
    def printHeaders(self):
        print(self.headers)

    def getFilename(self):
        return self.filename
    


