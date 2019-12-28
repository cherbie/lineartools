import json

class ConfigParser:
    def __init__(self, config):
        self.file = open(config, 'r')
        self.data = json.load(self.file)
        # print(self.data)
        self.file.close()
    
    def getMeta(self):
        meta = {
            'forms': self.data['FORMS'],
            'visits': self.data['VISITS']
        }
        return meta
    
    def getInputFile(self):
        return self.data['FILE']
    
    def getOutputFolder(self):
        return self.data['OUTPUT']
