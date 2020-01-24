from src import FileReader, FileWriterXL

def main():
    filename = input("Input filename/location:\n") # GET FILENAME / LOCATION

    # GET XLSX WORKBOOK METADATA
    wb_reader = FileReader(filename)
    sheetname = wb_reader.getSheetnames()[0]
    ws = wb_reader.getWorksheet(sheetname)
    headers = wb_reader.getSheetHeaders(sheetname)

    # GET THE COLUMN
    #col_num = input()
    id_col = 6

    # Look for participants
    participants = {}
    rows = ws.iter_rows(min_row=2, values_only=True)
    for row in rows:
        if row[id_col] is None:
            break
        elif row[id_col] == 'VOID':
            continue
        else:
            # parser.parseRow(row, subject)
            id = row[id_col]
            if participants.get(f'{id}', None) is None:
                participants[f'{id}'] = []
            values = {}
            for index, header in enumerate(headers):
                values[f'{header}'] = row[index]
            participants[f'{id}'].append(values)

    # CREATE OUTPUT FILE
    outputfilename = input('Output filename/location:\n')

    # WRITE TO FILE NEW SHEETS
    wb_writer = FileWriterXL(outputfilename, headers)
    for key, value in participants.items():
        print(key)
        wb_writer.bulkWriteSheet(key, value)

    wb_writer.close() # saves the document

main()
