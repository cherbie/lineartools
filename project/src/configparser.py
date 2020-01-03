import json

class ConfigParser:
    def __init__(self, config):
        self.file = open(config, 'r')
        self.data = json.load(self.file)
        self.file.close()
    
    def getInputHeaders(self):
        return self.data['INPUT'].get('COLUMNS', None)
    
    def getInputFile(self):
        return self.data['INPUT'].get('FILE', None)
    
    def getOutputFolder(self):
        return self.data['OUTPUT']
