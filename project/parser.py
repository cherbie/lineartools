from filewriter import FileWriter
from sheetparser import SheetParser

def workbookParser(wb_reader, config):
    '''
    Parse all subjects for a particular form and create output files
    @param wb_reader - FileReader object containing workbook file and meta information
    '''
    meta = config.getMeta()
    parser = SheetParser(meta) # object collating all information

    for subject in wb_reader.wb.sheetnames: # subject per worksheet
        ws = wb_reader.getWorksheet(subject) # subject sheet
        rows = ws.iter_rows(min_row=2, values_only=True)
        for row in rows:
            if row[0] is None:
                break
            elif row[0] == 'VOID':
                continue
            else:
                parser.parseRow(row, subject)

    # WRITE FORM DATA TO FILE
    for formname in meta['forms']:
        file = FileWriter(f'{config.getOutputFolder()}/{formname}', parser.getHeaders())
        file.bulkWrite(parser.getFormData(formname))
        file.close()
    
    return