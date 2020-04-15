from src import FileReader, FileWriterXL
import os

def main():
    filename = input("Input filename / location:\n") # GET FILENAME / LOCATION

    # CHECK THE INPUT FILE EXISTS
    if not os.path.exists(filename):
        raise Exception(f"Specified input file path does not exist ...\n{filename}")

    # GET XLSX WORKBOOK METADATA
    wb_reader = FileReader(filename)
    sheetname = wb_reader.getSheetnames()[0]
    ws = wb_reader.getWorksheet(sheetname)
    headers = wb_reader.getSheetHeaders(sheetname)

    # GET THE COLUMN
    #col_num = input("Column number of unique subject identifier: (Note: Column A = 0)\n")
    id_col = 6

    # Look for participants
    participants = {}
    rows = ws.iter_rows(min_row=2, max_row=4000, values_only=True)
    for row in rows:
        if row[id_col] is None:
            break
        elif row[id_col] == "":
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
    outputfilename = input('Output filename / location:\n')

    # WRITE TO FILE NEW SHEETS
    wb_writer = FileWriterXL(outputfilename, headers)
    for key, value in participants.items():
        print(key)
        wb_writer.bulkWriteSheet(key, value)

    wb_writer.close() # saves the document

try:
    main()
except Exception as err:
    print("An error has occurred!\n\n")
    print(err)
