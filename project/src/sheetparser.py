import re

class SheetParser:
    '''
    Model for the CSV file values
    '''

    COL_VISIT = 0
    COL_FORM = 1
    COL_ASSESS = 2
    COL_NUM = 3
    COL_REF = 4
    COL_DATE = 5
    COL_HEART = 9
    COL_RR = 10
    COL_P = 11
    COL_PR = 12
    COL_QRSD = 13
    COL_QT = 14
    COL_QTCF = 15
    YES = 'Yes'
    NO = 'No'

    def __init__(self, meta, inputHeaders=None, outputHeaders=None):
        self.meta = meta
        self.data = dict.fromkeys(self.meta['forms'])
        self.outputHeaders = outputHeaders
        if inputHeaders is None:
            self.inputHeaders = {} # empty
        else:
            self.inputHeaders = inputHeaders
    
    def parseRow(self, row, subject):
        '''
        Assuming external sorting on a per subject basis
        '''
        # GET FORMNAME
        formname = row[self.inputHeaders.get('FORM', self.COL_FORM)]
        if formname is None:
            raise 'No formname specified in row'
        elif self.data.get(formname, None) is None:
            self.data[formname] = dict.fromkeys(self.meta['visits']) # VISITS WILL CONTAIN UNIQUE DICTIONARY ENTRY
        
        visit = row[self.inputHeaders.get('VISIT', self.COL_VISIT)] # FETCH VISIT

        if self.data[formname].get(visit, None) is None: # DATA FOR SUBJECT AT VISIT NOT YET CONFIGURED
            self.data[formname][visit] = {
                f'{subject}': {
                    'SubjectID': subject,
                    'Form': formname,
                    'Visit': visit,
                }
            }
        elif self.data[formname][visit].get(subject, None) is None:
            self.data[formname][visit][subject] = {
                'SubjectID': subject,
                'Form': formname,
                'Visit': visit,
            }
        
        numref = self.inputHeaders.get('_NUM', self.COL_NUM) # ECG NUMBER WITHIN TRIPLICATE
        regmatch = re.search('#?R[13]', row[numref])
        
        # object
        self.data[formname][visit][subject][f'DatTim_{row[numref]}'] = row[self.inputHeaders.get('DATE', self.COL_DATE)]
        self.data[formname][visit][subject][f'Ref_{row[numref]}'] = row[self.inputHeaders.get('REF', self.COL_REF)]
        self.data[formname][visit][subject][f'Heart_{row[numref]}'] = row[self.inputHeaders.get('HEART', self.COL_HEART)]
        self.data[formname][visit][subject][f'RR_{row[numref]}'] = row[self.inputHeaders.get('RR', self.COL_RR)]
        self.data[formname][visit][subject][f'PR_{row[numref]}'] = row[self.inputHeaders.get('PR', self.COL_PR)]
        self.data[formname][visit][subject][f'QRSD_{row[numref]}'] = row[self.inputHeaders.get('QRSD', self.COL_QRSD)]
        self.data[formname][visit][subject][f'QT_{row[numref]}'] = row[self.inputHeaders.get('QT', self.COL_QT)]
        self.data[formname][visit][subject][f'QTcF_{row[numref]}'] = row[self.inputHeaders.get('QTCF', self.COL_QTCF)]
        self.data[formname][visit][subject][f'Assess_{row[numref]}'] = row[self.inputHeaders.get('ASSESSMENT', self.COL_ASSESS)]

        # Yes/No value for is repeat required
        if regmatch is not None and regmatch.string[regmatch.span()[1]-1]:
            self.data[formname][visit][subject][f'Repeat_{regmatch.string}'] = self.inputHeaders('YES', self.YES)

    
    def getFormData(self, formname='15MIN Predose 12 Lead ECG (Triplicate)'):
        formdata = []

        if formname is None: # IF NO FORMNAME IS PROVIDED
            formname = self.meta['forms'][0]
        
        if self.data.get(formname, None) is None: # FORM HAS NO DATA
            formdata.append({})
        else:
            for visit in self.data[formname]:
                if self.data[formname].get(visit, None) is None:
                    continue
                for subject in self.data[formname][visit]:
                    if self.data[formname][visit].get(subject, None) is None:
                        continue
                    formdata.append(self.data[formname][visit][subject])

        return formdata

    def getHeaders(self):
        if self.outputHeaders is None:
            return ('SubjectID', 'Form', 'Visit', 'DatTim_#1', 'Ref_#1', 'Heart_#1', 'RR_#1', 'PR_#1', 'QRSD_#1', 'QT_#1', 'QTcF_#1', 'Assess_#1', 'DatTim_#2', 'Ref_#2', 'Heart_#2', 'RR_#2', 'PR_#2', 'QRSD_#2', 'QT_#2', 'QTcF_#2', 'Assess_#2', 'DatTim_#3', 'Ref_#3', 'Heart_#3', 'RR_#3', 'PR_#3', 'QRSD_#3', 'QT_#3', 'QTcF_#3', 'Assess_#3', 'Repeat_#R1', 'DatTim_#R1', 'Ref_#R1', 'Heart_#R1', 'RR_#R1', 'PR_#R1', 'QRSD_#R1', 'QT_#R1', 'QTcF_#R1', 'Assess_#R1', 'DatTim_#R2', 'Ref_#R2', 'Heart_#R2', 'RR_#R2', 'PR_#R2', 'QRSD_#R2', 'QT_#R2', 'QTcF_#R2', 'Assess_#R2', 'Repeat_#R3', 'DatTim_#R3', 'Ref_#R3', 'Heart_#R3', 'RR_#R3', 'PR_#R3', 'QRSD_#R3', 'QT_#R3', 'QTcF_#R3', 'Assess_#R3', 'DatTim_#R4', 'Ref_#R4', 'Heart_#R4', 'RR_#R4', 'PR_#R4', 'QRSD_#R4', 'QT_#R4', 'QTcF_#R4', 'Assess_#R4')
        else:
            return self.outputHeaders


