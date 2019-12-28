import sys, os
from filereader import FileReader
from parser import workbookParser
from configparser import ConfigParser

def main():
    if len(sys.argv) < 2:
        print('Usage: python3 app.py configfilelocation')
        sys.exit()
    
    configFile = sys.argv[1]
    if not os.path.exists(configFile):
        raise IOError
    print(' ... reading config file')
    config = ConfigParser(configFile)
    print(' ... reading excel file')
    wb_reader = FileReader(config.getInputFile(), config.getMeta())
    print(' ... parsing file data')
    workbookParser(wb_reader, config) # business logic
    print(' ... process complete')

main()