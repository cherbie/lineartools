import sys, os, time
from src import FileReader, workbookParser, ConfigParser

errstr = 'AN ERROR HAS OCCURED!\n\nError reporting may have been provided above. Please correct these errors.\n\nWould you like to try again: (y/N)\n'

def main():
    if len(sys.argv) == 1:
        configFile = input('Location of CONFIG file (.json): ')
    elif len(sys.argv) > 2:
        print('Usage: python3 app.py configfilelocation')
        raise Exception('INCORRECT NUMBER OF ARGUMENTS SPECIFIED')
    else:
        configFile = sys.argv[1]
    
    if not os.path.exists(configFile):
        print('Configuration file could not be found. Please review the file path.')
        raise Exception('CONFIG FILE PATH ERROR. THE SPECIFIED PATH DOES NOT EXIST.\n')
    
    print(' ... reading config file')
    config = ConfigParser(configFile)
    print(' ... reading excel file')
    wb_reader = FileReader(config.getInputFile())
    print(' ... parsing file data')
    workbookParser(wb_reader, config) # business logic
    print(' ... process complete')
    time.sleep(10)
    sys.exit()

value = 'y'
while value == 'y':
    try:
        main()
    except Exception as err:
        print('--------------------')
        print(err)
        print('--------------------')
        value = input(errstr)
