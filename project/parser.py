from filewriter import FileWriter
from sheetparser import SheetParser

def workbookParser(wb_reader, headers=None):
    '''
    Parse all subjects for a particular form and create output files
    @param wb_reader - FileReader object containing workbook file and meta information
    '''
    header_template = ('SubjectID', 'Visit', 'FormName', 'DatTim_1', 'Ref_1', 'HR_1')
    
    parser = SheetParser(wb_reader.meta) # object collating all information

    for subject in wb_reader.wb.sheetnames:
        print(subject)
        ws = wb_reader.getWorksheet(subject) # subject sheet
        rows = ws.iter_rows(min_row=2, values_only=True)
        for row in rows:
            if row[0] is None:
                break
            elif row[0] == 'VOID':
                continue
            else:
                parser.parseRow(row, subject)
    print(parser.getFormData())

    for formname in wb_reader.meta['forms']:
        file = FileWriter(formname, parser.getHeaders())
        file.bulkWrite(parser.getFormData(formname))
        file.close()
        print(formname)
    
    # csv write
    return